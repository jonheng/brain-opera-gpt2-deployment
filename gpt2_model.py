import gpt_2_simple as gpt2

def get_single_response(prompt):
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess)
    response = gpt2.generate(sess, run_name='run1', prefix=prompt, top_k=40, length=50,
                            nsamples=1, batch_size=1, return_as_list=True)

    return response[0]

