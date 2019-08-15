import tensorflow as tf


def tf_health_check():
    return {'is_gpu_available': tf.test.is_gpu_available(),
            'is_built_with_cuda': tf.test.is_built_with_cuda()}

