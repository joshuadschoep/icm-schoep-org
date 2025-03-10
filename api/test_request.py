from request import Request
import pytest

class TestPayouts:
    def test_throws_error_on_0_payouts(self):
        with pytest.raises(ValueError):
            Request(payouts=[], players=[{ "stack": 1}])

    def test_throws_error_on_too_many_payouts(self):
        with pytest.raises(ValueError):
            Request(payouts=[12] * 13, players=[{ "stack": 1}] * 13)


class TestPlayers:
    def test_throws_error_on_0_players(self):
        with pytest.raises(ValueError):
            Request(payouts=[1], players=[])
    
    def test_throws_error_with_no_stack(self):
        with pytest.raises(ValueError):
            Request(payouts=[1], players=[{ "name": "Namerson" }])
    
    def test_allows_players_with_names(self):
        model = Request(payouts=[1], players=[{ "stack": 1, "name": "Namerson" }])
        assert len(model.players) == 1
    
    def test_requires_stack_to_be_integer_float(self):
        with pytest.raises(ValueError):
            Request(payouts=[1], players=[{ "stack": 100.1, "name": "Namerson" }])
    
    def test_requires_stack_to_be_integer_string(self):
        with pytest.raises(ValueError):
            Request(payouts=[1], players=[{ "stack": "oneHundred", "name": "Namerson" }])

    def test_requires_name_to_be_string_number(self):
        with pytest.raises(ValueError):
            Request(payouts=[1], players=[{ "stack": 100, "name": 123 }])        
    
    def test_requires_name_to_be_less_than_64(self):
        with pytest.raises(ValueError):
            Request(payouts=[1], players=[{ "stack": 100, "name": "a" * 64 }])

    def test_requires_name_to_be_greater_than_0(self):
        with pytest.raises(ValueError):
            Request(payouts=[1], players=[{ "stack": 100, "name": "" }])

    def test_requires_name_to_be_string_object(self):
        with pytest.raises(ValueError):
            Request(payouts=[1], players=[{ "stack": 100, "name": { "obj": "obj"} }])

    def test_throws_error_on_too_many_players(self):
        with pytest.raises(ValueError):
            Request(payouts=[12], players=[{ "stack": 1}] * 13)


class TestRelations:
    def test_allows_1_payout_with_1_player(self):
        model = Request(payouts=[1], players=[{ "stack": 1}])
        assert len(model.payouts) == 1

    def test_allows_2_payout_with_2_player(self):
        model = Request(payouts=[100, 200], players=[{ "stack": 200 }, { "stack":100}])
        assert len(model.payouts) == 2
    
    def test_allows_1_payout_with_2_players(self):
        model = Request(payouts=[200], players=[{ "stack": 200 }, { "stack":100}])
        assert len(model.payouts) == 1
    
    def test_throws_error_on_2_payouts_with_1_player(self):
        with pytest.raises(ValueError):
            Request(payouts=[100, 200], players=[{ "stack":100}])

    def test_throws_error_on_3_payouts_with_2_players(self):
        with pytest.raises(ValueError):
            Request(payouts=[100, 200, 300], players=[{ "stack":100}, { "stack": 200}])