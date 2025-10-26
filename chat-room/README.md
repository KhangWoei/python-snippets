# [Re]building environments
```
hatch env prune && hatch env create
```

# [Re]Building a specific environment
```
hatch env remove <environment> && hatch env create <environment>
```

# Running a script
```
hatch run <environment>:<script>
```

# Show existing environments
```
hatch env show
```

# On local deps
https://github.com/pypa/hatch/discussions/225
