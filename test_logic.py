from logic_engine import KnowledgeBase


def test_forward_chaining():
    kb = KnowledgeBase()

    kb.tell_rule(['TargetVisible', 'HasDust'], 'SafeToEngage')
    kb.tell_rule(['SafeToEngage', 'BloodseekerMissing'], 'Retreat')

    # Test 1: facts TargetVisible, HasDust -> SafeToEngage but not Retreat
    kb.clear_facts()
    kb.tell_fact('TargetVisible')
    kb.tell_fact('HasDust')
    kb.forward_chain()
    assert 'SafeToEngage' in kb.facts, "Test 1 failed: SafeToEngage should be derived"
    assert 'Retreat' not in kb.facts, "Test 1 failed: Retreat should not be derived"

    # Test 2: facts TargetVisible, HasDust, BloodseekerMissing -> Retreat
    kb.clear_facts()
    kb.tell_fact('TargetVisible')
    kb.tell_fact('HasDust')
    kb.tell_fact('BloodseekerMissing')
    kb.forward_chain()
    assert 'Retreat' in kb.facts, "Test 2 failed: Retreat should be derived"

    print("[OK] All Logic Engine Test Cases Passed!")


if __name__ == "__main__":
    test_forward_chaining()