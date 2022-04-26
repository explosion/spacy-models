def test_zh_tagger_spaces(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    doc = NLP("作为语言而言，为世界使用人数最多的语言，  目前世界有五分之一人口做\n\n为母语。")
    for t in doc:
        if t.is_space:
            assert t.pos_ == "SPACE"
            assert t.tag_ == "_SP"
        else:
            assert t.pos_ != "SPACE"
            assert t.tag_ != "_SP"


def test_zh_tagger_return_char(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    text = (
        "hi Aaron,\r\n\r\nHow is your schedule today, I was wondering if "
        "you had time for a phone\r\ncall this afternoon?\r\n\r\n\r\n"
    )
    doc = NLP(text)
    for t in doc:
        if t.is_space:
            assert t.pos_ == "SPACE"
