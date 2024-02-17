import g4f

providers = [
    provider.__name__
    for provider in g4f.Provider.__providers__
    if provider.working
]

print('self._providers = [')
for pro in providers:
    print(f"g4f.Provider.{pro},")
print(']')