import json
import os
from typing import List

from openai import OpenAI

from modules.ai_explaination.adapter.input.web.request.recommendation_explaination import (
    RecommendationItem,
)
from modules.ai_explaination.application.port.llm_port import LLMPort


class LLMAdapter(LLMPort):
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self._api_key:
            raise ValueError("OPENAI_API_KEY is not set")
        self._client = OpenAI(api_key=self._api_key)
        self._model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def finder_recommendation_reasons(
            self,
            recommendation: RecommendationItem,
            query_summary: str,
            tone: str = "formal",  # 파라미터 추가
    ) -> List[str]:
        listing_context = recommendation.model_dump(exclude_none=True)

        # 말투에 따른 시스템 프롬프트
        if tone == "casual":
            tone_instruction = "반말(~이야, ~해, ~거야)로 답변하세요."
        else:
            tone_instruction = "존댓말(~입니다, ~합니다)로 답변하세요."

        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"당신은 한국어로 답변하는 부동산 어시스턴트야. "
                        f"{tone_instruction} "
                        f"대학생인 임차인 요청과 매물 정보를 기반으로 이 매물을 추천하는 이유를 "
                        f"간결하게 제시하세요. 출력은 2~4개의 짧은 한국어 문장으로 이루어진 "
                        f"JSON 배열만 반환합니다. 다른 설명이나 텍스트를 덧붙이지 마세요."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Renter request summary: {query_summary}\n"
                        f"Listing data (JSON): {json.dumps(listing_context, ensure_ascii=False)}\n"
                        "Return only the JSON array of reasons."
                    ),
                },
            ],
            temperature=0.3,
        )

        content = response.choices[0].message.content or "[]"
        reasons = self._parse_reason_list(content)
        if reasons:
            return reasons

        # 실패 메시지도 말투 적용
        if tone == "casual":
            return ["추천 이유를 생성하지 못했어."]
        return ["추천 이유를 생성하지 못했습니다."]

        # 2. 신규 메서드 (임대인에게 세입자 추천)
     def owner_recommendation_reasons(
                self,
                house: RecommendationItem,
                tenant: TenantCandidateItem,
                tone: str = "formal"
        ) -> List[str]:

            tone_instruction = "정중한 해요체(~해요)로" if tone != "casual" else "친근한 반말(~야)로"

            # 임대인용 프롬프트 설계
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"당신은 임대 관리 전문가입니다. {tone_instruction} "
                            "임대인의 매물 정보와 세입자 후보 정보를 비교하여, "
                            "임대인에게 '이 세입자를 받아야 하는 이유'를 설득력 있게 설명하세요. "
                            "월세 지불 능력(예산)과 거주 성향을 중심으로 3가지 이유를 작성하세요. "
                            "출력은 반드시 JSON 배열([\"이유1\", \"이유2\"]) 형태여야 합니다."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"[내 매물 정보]\n"
                            f"- 월세: {house.monthly_rent}만원 (보증금 {house.deposit})\n"
                            f"- 매물명: {house.title}\n\n"
                            f"[세입자 후보]\n"
                            f"- 직업: {tenant.job_status}\n"
                            f"- 희망 예산: 월세 {tenant.budget_monthly}만원\n"
                            f"- 학교: {tenant.university}\n"
                            f"- 특징: {', '.join(tenant.lifestyle_tags)}\n\n"
                            "위 정보를 바탕으로 추천 사유를 JSON 배열로 생성하세요."
                        ),
                    },
                ],
                temperature=0.3,
            )

            content = response.choices[0].message.content or "[]"
            return self._parse_reason_list(content)

    def _parse_reason_list(self, content: str) -> List[str]:
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = None

        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed if str(item).strip()]

        lines = [line.strip(" -•\t") for line in content.splitlines()]
        return [line for line in lines if line]