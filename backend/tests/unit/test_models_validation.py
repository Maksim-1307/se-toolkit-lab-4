"""Unit tests for model validation edge cases and boundary values."""

from datetime import datetime

from app.models.interaction import InteractionLog, InteractionLogCreate
from app.models.item import ItemCreate, ItemUpdate
from app.models.learner import LearnerCreate


class TestItemCreateValidation:
    """Tests for ItemCreate schema validation edge cases."""

    def test_empty_title_is_accepted(self) -> None:
        """Empty title is accepted by Pydantic str type (no validation).
        
        Note: Pydantic v2's str type does not enforce non-empty strings.
        Validation for empty titles should be done at the API layer.
        """
        item = ItemCreate(title="")
        assert item.title == ""

    def test_whitespace_only_title_is_accepted(self) -> None:
        """Title with only whitespace is accepted by Pydantic str type.
        
        Note: Pydantic v2's str type does not strip or validate whitespace.
        """
        item = ItemCreate(title="   ")
        assert item.title == "   "

    def test_title_with_special_characters_is_accepted(self) -> None:
        """Title with special characters should be accepted."""
        item = ItemCreate(title="Lab #1: Intro to <Python> & 'Data'")
        assert item.title == "Lab #1: Intro to <Python> & 'Data'"

    def test_title_with_unicode_characters_is_accepted(self) -> None:
        """Title with unicode characters should be accepted."""
        item = ItemCreate(title="日本語タイトル 🚀")
        assert item.title == "日本語タイトル 🚀"

    def test_very_long_title_is_accepted(self) -> None:
        """Very long titles should be accepted (boundary test)."""
        long_title = "A" * 1000
        item = ItemCreate(title=long_title)
        assert len(item.title) == 1000

    def test_parent_id_zero_is_accepted(self) -> None:
        """parent_id of 0 should be accepted (boundary value)."""
        item = ItemCreate(title="Child Item", parent_id=0)
        assert item.parent_id == 0

    def test_negative_parent_id_is_accepted(self) -> None:
        """Negative parent_id should be accepted (edge case)."""
        item = ItemCreate(title="Child Item", parent_id=-1)
        assert item.parent_id == -1

    def test_default_type_is_step(self) -> None:
        """Default type should be 'step'."""
        item = ItemCreate(title="Default Item")
        assert item.type == "step"

    def test_empty_description_defaults_to_empty_string(self) -> None:
        """Empty description should default to empty string."""
        item = ItemCreate(title="Item", description="")
        assert item.description == ""


class TestItemUpdateValidation:
    """Tests for ItemUpdate schema validation edge cases."""

    def test_empty_title_is_accepted(self) -> None:
        """Empty title is accepted by Pydantic str type."""
        item = ItemUpdate(title="")
        assert item.title == ""

    def test_whitespace_only_title_is_accepted(self) -> None:
        """Title with only whitespace is accepted by Pydantic str type."""
        item = ItemUpdate(title="   ")
        assert item.title == "   "

    def test_empty_description_is_accepted(self) -> None:
        """Empty description should be accepted."""
        item = ItemUpdate(title="Updated Item", description="")
        assert item.description == ""


class TestLearnerCreateValidation:
    """Tests for LearnerCreate schema validation edge cases."""

    def test_empty_name_is_accepted(self) -> None:
        """Empty name is accepted by Pydantic str type (no validation).
        
        Note: Validation for empty names should be done at the API layer.
        """
        learner = LearnerCreate(name="", email="test@example.com")
        assert learner.name == ""

    def test_whitespace_only_name_is_accepted(self) -> None:
        """Name with only whitespace is accepted by Pydantic str type."""
        learner = LearnerCreate(name="   ", email="test@example.com")
        assert learner.name == "   "

    def test_empty_email_is_accepted(self) -> None:
        """Empty email is accepted by Pydantic str type (no validation)."""
        learner = LearnerCreate(name="Test User", email="")
        assert learner.email == ""

    def test_invalid_email_format_is_accepted_by_pydantic(self) -> None:
        """
        Pydantic v2's str type doesn't enforce email format by default.
        This tests that the schema accepts any string as email.
        Email validation should be done at the API layer if needed.
        """
        learner = LearnerCreate(name="Test User", email="not-an-email")
        assert learner.email == "not-an-email"

    def test_email_with_special_characters_is_accepted(self) -> None:
        """Email with plus addressing should be accepted."""
        learner = LearnerCreate(name="Test User", email="user+tag@example.com")
        assert learner.email == "user+tag@example.com"

    def test_name_with_unicode_characters_is_accepted(self) -> None:
        """Name with unicode characters should be accepted."""
        learner = LearnerCreate(name="田中太郎", email="tanaka@example.com")
        assert learner.name == "田中太郎"

    def test_very_long_name_is_accepted(self) -> None:
        """Very long names should be accepted (boundary test)."""
        long_name = "A" * 500
        learner = LearnerCreate(name=long_name, email="test@example.com")
        assert len(learner.name) == 500


class TestInteractionLogCreateValidation:
    """Tests for InteractionLogCreate schema validation edge cases."""

    def test_empty_kind_is_accepted(self) -> None:
        """Empty kind is accepted by Pydantic str type (no validation).
        
        Note: Validation for empty kind should be done at the API layer.
        """
        interaction = InteractionLogCreate(learner_id=1, item_id=1, kind="")
        assert interaction.kind == ""

    def test_whitespace_only_kind_is_accepted(self) -> None:
        """Kind with only whitespace is accepted by Pydantic str type."""
        interaction = InteractionLogCreate(learner_id=1, item_id=1, kind="   ")
        assert interaction.kind == "   "

    def test_very_long_kind_is_accepted(self) -> None:
        """Very long kind should be accepted (boundary test)."""
        long_kind = "a" * 500
        interaction = InteractionLogCreate(
            learner_id=1, item_id=1, kind=long_kind
        )
        assert len(interaction.kind) == 500

    def test_zero_learner_id_is_accepted(self) -> None:
        """learner_id of 0 should be accepted (boundary value)."""
        interaction = InteractionLogCreate(learner_id=0, item_id=1, kind="view")
        assert interaction.learner_id == 0

    def test_negative_learner_id_is_accepted(self) -> None:
        """Negative learner_id should be accepted by schema (edge case)."""
        interaction = InteractionLogCreate(learner_id=-1, item_id=1, kind="view")
        assert interaction.learner_id == -1

    def test_zero_item_id_is_accepted(self) -> None:
        """item_id of 0 should be accepted (boundary value)."""
        interaction = InteractionLogCreate(learner_id=1, item_id=0, kind="view")
        assert interaction.item_id == 0

    def test_negative_item_id_is_accepted(self) -> None:
        """Negative item_id should be accepted by schema (edge case)."""
        interaction = InteractionLogCreate(learner_id=1, item_id=-1, kind="view")
        assert interaction.item_id == -1

    def test_kind_with_special_characters_is_accepted(self) -> None:
        """Kind with special characters should be accepted."""
        interaction = InteractionLogCreate(
            learner_id=1, item_id=1, kind="click-button#submit"
        )
        assert interaction.kind == "click-button#submit"


class TestInteractionLogModel:
    """Tests for InteractionLog model edge cases."""

    def test_created_at_can_be_none(self) -> None:
        """InteractionLog can have None created_at."""
        log = InteractionLog(
            id=1, learner_id=1, item_id=1, kind="view", created_at=None
        )
        assert log.created_at is None


class TestFilterByItemIdEdgeCases:
    """Edge case tests for _filter_by_item_id function."""

    @staticmethod
    def _make_log(
        id: int, learner_id: int, item_id: int
    ) -> InteractionLog:
        return InteractionLog(
            id=id, learner_id=learner_id, item_id=item_id, kind="attempt"
        )

    def test_filter_with_negative_item_id(self) -> None:
        """Filtering with negative item_id should return empty list.
        
        Note: This tests the edge case where item_id is negative.
        The filter function uses exact equality matching.
        """
        from app.routers.interactions import _filter_by_item_id
        interactions = [
            self._make_log(1, 1, 1),
            self._make_log(2, 1, 2),
        ]
        result = _filter_by_item_id(interactions, -1)
        assert result == []

    def test_filter_with_zero_item_id(self) -> None:
        """Filtering with item_id=0 should return matching interactions.
        
        Note: This tests the boundary value of 0 for item_id.
        """
        from app.routers.interactions import _filter_by_item_id
        interactions = [
            self._make_log(1, 1, 0),
            self._make_log(2, 1, 1),
        ]
        result = _filter_by_item_id(interactions, 0)
        assert len(result) == 1
        assert result[0].id == 1

    def test_filter_returns_multiple_matches(self) -> None:
        """Filter should return all interactions matching the item_id.
        
        Note: This tests that multiple interactions with the same item_id
        are all returned, not just the first match.
        """
        from app.routers.interactions import _filter_by_item_id
        interactions = [
            self._make_log(1, 1, 1),
            self._make_log(2, 2, 1),
            self._make_log(3, 3, 2),
            self._make_log(4, 1, 1),
        ]
        result = _filter_by_item_id(interactions, 1)
        assert len(result) == 3
        assert all(i.item_id == 1 for i in result)

    def test_filter_preserves_original_order(self) -> None:
        """Filter should preserve the original order of interactions.
        
        Note: This tests that the filtered results maintain their
        original ordering from the input list.
        """
        from app.routers.interactions import _filter_by_item_id
        interactions = [
            self._make_log(1, 1, 1),
            self._make_log(2, 2, 2),
            self._make_log(3, 1, 1),
        ]
        result = _filter_by_item_id(interactions, 1)
        assert [i.id for i in result] == [1, 3]
