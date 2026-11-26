def test_alignement_coups_theoriques():
    # Exemple basé sur votre logique précédente
    raw_is_book = [True, True, False]  # Inclut la position de départ
    aligned_is_book = raw_is_book[1:]

    assert len(aligned_is_book) == 2
    assert aligned_is_book == [True, False]
