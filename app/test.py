from app import hello
def on_raw_message(body):
    print(body)

a, b = 1, 1
r = hello.apply_async(args=(a, b),task_id="2f43fef3-b3e1-440c-b9de-7c269970e639")
print(r.get(on_message=on_raw_message, propagate=False))