from Wrapper import Wrapper

# initalize program and ask for information to start retrieve data from the API of overheid.io
#company = Wrapper('Bejo Zaden B.V.')  # Test gemeente Utrecht, #Test Triple - A rk finance

#companies = dict([(name, Wrapper(name).data) for name in ['AB WERKT DETACHERING B.V.']])

companies = Wrapper('PROFOURCE SERVICE CENTER B.V.').data

print(companies)

