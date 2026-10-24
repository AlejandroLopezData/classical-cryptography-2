from measure import index_of_coincidence

txt50 = "THEWEATHERWASCOLDANDTHESTREETSWEREEMPTYWHENSHECAME"
txt80 = "THEWEATHERWASCOLDANDTHESTREETSWEREEMPTYWHENSHEWALKEDHOMEFROMTHESTATIONANDSAWTHEM"
txt100 = "THEWEATHERWASCOLDANDTHESTREETSWEREEMPTYWHENSHEWALKEDHOMEFROMTHESTATIONANDSAWALIGHTINTHEWINDOWOFTHEIR"


def test_ioc():
    print("-----------------------------------")
    print("Index of coincidence tests")
    print("-----------------------------------")
    print("CRYPTANALYSIS:",index_of_coincidence("CRYPTANALYSIS")) 
    print("THEINDEXOFCOINCIDENCE:",index_of_coincidence("THEINDEXOFCOINCIDENCE")) 
    print("txt50:",index_of_coincidence(txt50))
    print("txt80:",index_of_coincidence(txt80))
    print("txt100:",index_of_coincidence(txt100))
    print("-----------------------------------")

test_ioc()





#   Execute
#   python -m pytest tests/measure_IC_test.py
#   python -m tests.measure_IC_test
