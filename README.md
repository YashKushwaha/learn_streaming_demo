## Overview

This is a simple project to demonstrate how to stream LLM response to the front.

### Preparing the backend

Actual LLM call is simulated by the following function which echos user query word by word

```python
async def llm_call(message):
    for word in message.split():
        yield word + " "
        await asyncio.sleep(0.3)  # simulate delay
```

When post request is made to the chat end point, we process the user query and return a StreamingResponse from `fastapi.responses`

```python
@app.post("/echo")
async def echo_stream(request: Request):
    data = await request.json()
    message = data.get("message", "")
    dummy_llm_response = llm_call(message)
    return StreamingResponse(dummy_llm_response, media_type="text/plain")
```

### Preparing the front end

We make the POST request to backend using the regular syntax
```javascript
const response = await fetch(chatEndpoint, {
method: "POST",
headers: { "Content-Type": "application/json" },
body: JSON.stringify({ message: msg })
});
```
Since backend returns a [`ReadableStream`](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream), we can create a reader that locks the stream to it. 
```javascript
const reader = response.body.getReader();
```
We can call `.read()` method of the reader to access the data stream. It returns an object containing 2 properties:

- value - The data chunk from the stream
- done - boolean indicating whether the stream has finished (true)

We also need to decoder to convert the data type of value into plain text 
```javascript
const decoder = new TextDecoder("utf-8");
```

Now we can create a while loop that only breaks when `done` becomes `true`. Also we can increment the HTML inside the container displaying this output to the user.
```javascript
while (true) {
const { value, done } = await reader.read();
if (done) break;
output.innerHTML += decoder.decode(value, { stream: true });
}
```