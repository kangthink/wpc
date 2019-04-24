import pytest

import wpc

@pytest.mark.parametrize("test_input",[
   ('apple'), ('banana'), ('create')
])
def test_should_return_correct_not_none_str(test_input):
    assert wpc.audioFileURL(test_input)

@pytest.mark.parametrize("test_input",[
   ('av332'), ('#@#'), (' '), ('\n')
])
def test_should_raise_error_when_no_dictionary_data(test_input):
    with pytest.raises(wpc.NoLinkError) as e:
        wpc.audioFileURL(test_input)
