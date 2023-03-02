import os
import openai
import gradio as gr

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_answer(prompt, role):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": role, "content": prompt}
        ],
        temperature=0.7
    )
    message = completion.choices[0].message
    return message["content"].strip()


def clean_textbox(*args):
    n = len(args)
    return [""] * n


if __name__ == '__main__':
    with gr.Blocks(title="ChatGPT") as demo:
        gr.Markdown('''
        # ChatGPT
                ''')
        with gr.Row():
            with gr.Column(scale=9):
                prompt = gr.Text(label='ChatGPT_Prompt', show_label=False, lines=3,
                                 placeholder='ChatGPT Prompt')
                res = gr.Text(label='ChatGPT_result', show_label=False, lines=3,
                              placeholder='chatgpt results')

            with gr.Column(scale=1):
                role = gr.Dropdown(choices=['system', 'user', 'assistant'], value='assistant', label='role', interactive=True)
                btn_gen = gr.Button(value="Generate", variant='primary')
                btn_clear = gr.Button(value="Clear")

        gr.Examples([
            ["如何成为魔法少女"],
            ["假设有一个池塘，里面有无穷多的水。现有2个空水壶，容积分别为5升和6升。问题是如何只用这2个水壶从池塘里取得3升的水。"],
            ["请帮我用C++写出快排的代码。"]],
            inputs=[prompt],
            outputs=[res],
            fn=generate_answer,
            cache_examples=False)

        btn_gen.click(fn=generate_answer, inputs=[prompt, role],
                      outputs=res)
        btn_clear.click(fn=clean_textbox,
                        inputs=[prompt, res],
                        outputs=[prompt, res])

    demo.queue()
    demo.launch()
