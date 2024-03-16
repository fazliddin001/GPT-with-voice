import environs

env = environs.Env()
env.read_env(".env")
openai_key = env.str('OPENAI_KEY')
