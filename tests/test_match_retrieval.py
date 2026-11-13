import unittest
from unittest.mock import Mock, patch

from app.nodes import match
from app.state import BusinessModel, ProcessStep, RunState, StepRating, StepRatings


class RetrievalGateTests(unittest.TestCase):
    def test_leave_it_ratings_still_search_and_survive_selection_failure(self):
        steps = [
            ProcessStep(
                name=f"Step {i}", data_input="Records", data_output="Reviewed records",
                likely_system="unknown", status="abgeleitet", evidence="industry",
            )
            for i in range(8)
        ]
        ratings = [
            StepRating(
                step=step.name, error_cost="high", knowledge="tacit", opportunity="bottleneck",
                money_lever="unit_cost", process_quality="leave it", score=i,
                reasoning="Physical work stays with people; information assistance needs evaluation.",
            )
            for i, step in enumerate(steps)
        ]
        state = RunState(
            company_name="Manufacturer", company_url="https://example.com",
            model=BusinessModel(
                company_type="Manufacturer", business_model=[], unit_economics=[],
                process_map=steps, open_numbers=[],
            ),
        )
        llm = Mock()
        llm.with_structured_output.return_value.invoke.return_value = StepRatings(ratings=ratings)
        card = {"id": "information-support", "title": "Review records", "approach": "quick win"}
        with (
            patch.object(match, "llm", return_value=llm),
            patch.object(match.library, "search", return_value=[card]) as search,
            patch.object(match, "_rerank_for_step", side_effect=lambda s, q, n, cards: cards),
            patch.object(match, "_picks_schema", side_effect=ValueError("Selection unavailable")),
        ):
            result = match.match_use_cases(state)
        self.assertEqual(search.call_count, match.TOP_STEPS)
        self.assertEqual(len(result["candidates"]), match.TOP_STEPS)
        self.assertEqual(result["ratings"], ratings)
        self.assertIsNone(result["picks"])
        self.assertIn("Selection unavailable", result["notes"][-1])
        self.assertEqual({r.process_quality for r in result["ratings"]}, {"leave it"})

    def test_unknown_step_ratings_do_not_enter_retrieval(self):
        rating = StepRating(
            step="Invented step", error_cost="low", knowledge="explicit", opportunity="repetitive",
            money_lever="unit_cost", process_quality="automate as-is", score=9, reasoning="Test",
        )
        self.assertEqual(match._rank_for_retrieval([rating], {"Actual step"}), [])


if __name__ == "__main__":
    unittest.main()
