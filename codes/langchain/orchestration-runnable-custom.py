import asyncio
import time

from langchain_core.runnables import RunnableLambda

# 2. Runnable with Python Lambda Function: Invoke, Batch, Stream
runnable_function = RunnableLambda(lambda x: x.strip()[3:])

invoked_result = runnable_function.invoke("   What does Hello World do in IT world ")
print(invoked_result)

batched_result_list = runnable_function.batch(
  [
    "  Abracadabra Irwoensa",
    "근데 한글도 되나?????",
    " Todwwq"
  ]
)
print(batched_result_list)

streamed_result = runnable_function.stream("""
                                           Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed gravida purus ut lorem finibus gravida. Proin vel erat et justo elementum pretium. Donec at convallis felis. Quisque maximus mauris magna. Suspendisse a tortor sit amet justo pulvinar elementum. Integer eget erat nisi. Sed eleifend, sapien quis efficitur rhoncus, dui dui fringilla dolor, sit amet lobortis metus dui at tellus. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aenean posuere convallis blandit. Ut sagittis urna magna, non pharetra magna ultrices a.

Pellentesque eleifend cursus congue. Integer eget facilisis sapien. Ut suscipit dui est, at porta est rhoncus nec. Nam blandit vel ante eu blandit. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sollicitudin pharetra dictum. Phasellus in luctus tellus.

Duis nec ipsum quis sem pulvinar ultrices vel non tellus. Ut non erat felis. Ut ex turpis, sodales non ullamcorper id, efficitur vitae nisl. Suspendisse posuere ex fermentum elit tempor malesuada. In blandit, purus nec iaculis ultricies, eros felis vehicula nulla, vel bibendum mauris velit quis tellus. Duis quis egestas erat, eget lacinia libero. Nam egestas euismod leo quis accumsan. Praesent congue, enim non accumsan pulvinar, risus mi cursus nibh, sit amet auctor libero nisl id felis. Nam diam velit, eleifend quis nibh eu, varius vestibulum arcu. Cras lobortis faucibus malesuada. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nullam varius facilisis ante eu fringilla. Donec fermentum lacus metus, ac vestibulum quam feugiat vel. Morbi ut sem scelerisque, volutpat mi ut, molestie neque. Integer et augue neque. In et nibh pretium, laoreet dui eget, bibendum lectus.

Mauris sit amet mauris lacus. Suspendisse non elementum purus, et tincidunt lacus. Suspendisse quis pharetra justo. Etiam eu diam sit amet tortor consequat placerat. Aenean bibendum auctor leo a mattis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse porttitor eros vel nulla sodales lacinia. Pellentesque pharetra dui a est placerat, et porttitor erat rhoncus. Etiam tristique quam lacus, sed accumsan sapien aliquet at. Donec auctor tortor sed mi ultricies finibus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Quisque sollicitudin turpis erat, quis suscipit ligula commodo non. Fusce pretium lacinia posuere.

In a libero quis ligula hendrerit varius quis non odio. Curabitur eleifend facilisis augue eget pellentesque. Duis at urna in nunc sollicitudin bibendum. Nam justo risus, placerat id varius gravida, sodales vel magna. Sed rhoncus malesuada felis vel commodo. Maecenas dignissim maximus commodo. Maecenas sollicitudin orci a nulla ornare, at facilisis nisi sollicitudin. Vivamus sed arcu at velit commodo rhoncus sed quis eros. Pellentesque porttitor lacus ornare urna viverra, vitae mollis nisi elementum. Maecenas mollis efficitur magna, a eleifend dui fermentum interdum. Vestibulum ligula nisl, facilisis vitae libero vitae, ultrices consequat velit. Etiam molestie nisl orci, eu pretium nisi hendrerit sit amet. Nullam in ultrices tellus. Sed arcu velit, mattis nec euismod in, porta a nisl. Donec sed molestie sapien, a tempor velit.
                                           """)

for chunk in streamed_result:
  print(chunk)
print()
  
# 2. Runnable with Function
def text_transformation(text: str) -> str:
  return " ".join( [token+"yo" for token in text[::-1].capitalize().replace(".","").strip().split(" ")])

text_transformation_runnable = RunnableLambda(text_transformation)

print(text_transformation_runnable.invoke("I want to go home."))
print(text_transformation_runnable.batch(
  [
    "Schools never teaches how to make money",
    "Company never teaches how to work",
    "And I want to go home"
  ]
))
print(text_transformation_runnable.stream("aslkjnwq inqwionqwe opwqjpwqoncqwoin wqqwpoijdrpqwoin wqo nqwlkn qwlqwn lkniqwio qnwwpoqin fwqini weblkg baerkgb lkreb iaerubg iabrelk "))

batch_async_inputs = [
  "qw lqm buu","si wnbvq wocw", "evbnl,k woowd qc"
]
async def run_async():
  aresult = await text_transformation_runnable.ainvoke("Broke Back Mountain")
  aresult = await text_transformation_runnable.abatch(batch_async_inputs)
  print(aresult)
  

asyncio.run(run_async())