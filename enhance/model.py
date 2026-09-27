from tensorflow.python.ops.image_ops_impl import adjust_gamma

import utils

import cv2 as cv

import time
import os
import numpy as np
import tensorflow as tf
from ops import *

#memory allocatio
# conf = tf.ConfigProto()
# conf.gpu_options.allow_growth=True
# session = tf.Session(config=conf)

tf.config.set_visible_devices([], 'GPU')

class T_CNN(object):

  def __init__(self,
               sess,
               image_height=460,
               image_width=620,
               label_height=460,
               label_width=620,
               batch_size=1,
               c_dim=3,
               c_depth_dim=1,
               checkpoint_dir=None,
               sample_dir=None,
               test_image_name = None,
               test_wb_name = None,
               test_ce_name = None,
               test_gc_name = None,
               id = None
               ):

    self.sess = sess
    self.is_grayscale = (c_dim == 1)
    self.image_height = image_height
    self.image_width = image_width
    self.label_height = label_height
    self.label_width = label_width
    self.batch_size = batch_size
    self.dropout_keep_prob=0.5
    self.test_image_name = test_image_name
    self.test_wb_name = test_wb_name
    self.test_ce_name = test_ce_name
    self.test_gc_name = test_gc_name
    self.id = id
    self.c_dim = c_dim
    self.df_dim = 64
    self.checkpoint_dir = checkpoint_dir
    self.build_model()

  def build_model(self):
    self.images = tf.compat.v1.placeholder(tf.float32, [self.batch_size, self.image_height, self.image_width, self.c_dim], name='images')
    self.images_wb = tf.compat.v1.placeholder(tf.float32, [self.batch_size, self.image_height, self.image_width, self.c_dim], name='images_wb')
    self.images_ce = tf.compat.v1.placeholder(tf.float32, [self.batch_size, self.image_height, self.image_width, self.c_dim], name='images_ce')
    self.images_gc = tf.compat.v1.placeholder(tf.float32, [self.batch_size, self.image_height, self.image_width, self.c_dim], name='images_gc')
    self.pred_h = self.model()


    self.saver = tf.compat.v1.train.Saver()

  def train(self, config):
    # 读取原始图像
    image_testm = cv.imread(self.test_image_name, cv.IMREAD_COLOR)
    if image_testm is None:
      print(f"Error: Could not read image: {self.test_image_name}")
      return False
      
    image_test = cv.cvtColor(image_testm, cv.COLOR_BGR2RGB) / 255
    shape = image_test.shape
    expand_test = image_test[np.newaxis,:,:,:]
    expand_zero = np.zeros([self.batch_size-1,shape[0],shape[1],shape[2]])
    batch_test_image = np.append(expand_test,expand_zero,axis = 0)

    print(f"Processing image: {self.test_image_name}, shape: {shape}")
    
    # 使用传入的白平衡图像文件（如果存在）
    if self.test_wb_name and os.path.exists(self.test_wb_name):
      print(f"Using provided white balance image: {self.test_wb_name}")
      wb_test_img = cv.imread(self.test_wb_name, cv.IMREAD_COLOR)
      wb_test = cv.cvtColor(wb_test_img, cv.COLOR_BGR2RGB) / 255
    else:
      print("Generating white balance image")
      wb_test = white_balance(image_testm, 0.5)
      wb_test = cv.cvtColor(wb_test, cv.COLOR_BGR2RGB) / 255
      
    shape_wb = wb_test.shape
    expand_test_wb = wb_test[np.newaxis,:,:,:]
    expand_zero_wb = np.zeros([self.batch_size-1,shape_wb[0],shape_wb[1],shape_wb[2]])
    batch_test_wb = np.append(expand_test_wb,expand_zero_wb,axis = 0)

    # 使用传入的对比度增强图像文件（如果存在）
    if self.test_ce_name and os.path.exists(self.test_ce_name):
      print(f"Using provided contrast enhanced image: {self.test_ce_name}")
      ce_test_img = cv.imread(self.test_ce_name, cv.IMREAD_COLOR)
      ce_test = cv.cvtColor(ce_test_img, cv.COLOR_BGR2RGB) / 255
    else:
      print("Generating contrast enhanced image")
      ce_test = cv.cvtColor(image_testm, cv.COLOR_BGR2GRAY)
      clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
      ce_test = clahe.apply(ce_test)
      ce_test = cv.cvtColor(ce_test, cv.COLOR_GRAY2BGR)
      ce_test = cv.cvtColor(ce_test, cv.COLOR_BGR2RGB) / 255
      
    shape_ce = ce_test.shape
    expand_test_ce = ce_test[np.newaxis,:,:,:]
    expand_zero_ce = np.zeros([self.batch_size-1,shape_ce[0],shape_ce[1],shape_ce[2]])
    batch_test_ce = np.append(expand_test_ce,expand_zero_ce,axis = 0)

    # 使用传入的伽马校正图像文件（如果存在）
    if self.test_gc_name and os.path.exists(self.test_gc_name):
      print(f"Using provided gamma corrected image: {self.test_gc_name}")
      gc_test_img = cv.imread(self.test_gc_name, cv.IMREAD_COLOR)
      gc_test = cv.cvtColor(gc_test_img, cv.COLOR_BGR2RGB) / 255
    else:
      print("Generating gamma corrected image")
      gc_test = adjust_gamma(image_testm, 0.7)
      gc_test = cv.cvtColor(gc_test, cv.COLOR_BGR2RGB) / 255
      
    shape_gc = gc_test.shape
    expand_test_gc = gc_test[np.newaxis,:,:,:]
    expand_zero_gc = np.zeros([self.batch_size-1,shape_gc[0],shape_gc[1],shape_gc[2]])
    batch_test_gc = np.append(expand_test_gc,expand_zero_gc,axis = 0)

    # 初始化变量
    tf.compat.v1.global_variables_initializer().run()

    # 加载模型
    if self.load(self.checkpoint_dir):
      print(" [*] Load SUCCESS")
    else:
      print(" [!] Load failed...")
      return False
      
    # 运行模型推理
    start_time = time.time()
    result_h = self.sess.run(self.pred_h, feed_dict={
        self.images: batch_test_image,
        self.images_wb: batch_test_wb,
        self.images_ce: batch_test_ce,
        self.images_gc: batch_test_gc
    })
    all_time = time.time()
    final_time = all_time - start_time
    print(f"Inference time: {final_time:.4f} seconds")

    # 处理结果
    _,h ,w , c = result_h.shape
    result_h0 = result_h[0,:,:,:].reshape(h, w, 3)
    result_h0 = result_h0.squeeze()
    
    # 获取文件名（不含路径）
    output_name = os.path.basename(self.test_image_name)
    
    # 直接保存到static/images/enhanced目录
    enhanced_dir = os.path.join(os.getcwd(), "static", "images", "enhanced")
    os.makedirs(enhanced_dir, exist_ok=True)
    enhanced_path = os.path.join(enhanced_dir, output_name)
    
    print(f"Saving result to: {enhanced_path}")
    imsave_lable(result_h0, enhanced_path)
    
    # 返回处理后的图像数据（值范围为[0,1]）
    print("Returning processed image data")
    return result_h0



  def model(self):


    with tf.compat.v1.variable_scope("main_branch") as scope:

      conb0 = tf.concat(axis = 3, values = [self.images,self.images_wb,self.images_ce,self.images_gc])
      conv_wb1 = tf.nn.relu(conv2d(conb0, 16,128, k_h=7, k_w=7, d_h=1, d_w=1,name="conv2wb_1"))
      conv_wb2 = tf.nn.relu(conv2d(conv_wb1, 128,128, k_h=5, k_w=5, d_h=1, d_w=1,name="conv2wb_2"))
      conv_wb3 = tf.nn.relu(conv2d(conv_wb2, 128,128, k_h=3, k_w=3, d_h=1, d_w=1,name="conv2wb_3"))
      conv_wb4 = tf.nn.relu(conv2d(conv_wb3, 128,64, k_h=1, k_w=1, d_h=1, d_w=1,name="conv2wb_4"))
      conv_wb5 = tf.nn.relu(conv2d(conv_wb4, 64,64, k_h=7, k_w=7, d_h=1, d_w=1,name="conv2wb_5"))
      conv_wb6 = tf.nn.relu(conv2d(conv_wb5, 64,64, k_h=5, k_w=5, d_h=1, d_w=1,name="conv2wb_6"))
      conv_wb7 = tf.nn.relu(conv2d(conv_wb6, 64,64, k_h=3, k_w=3, d_h=1, d_w=1,name="conv2wb_7"))

      conv_wb77 =tf.nn.sigmoid(conv2d(conv_wb7, 64,3, k_h=3, k_w=3, d_h=1, d_w=1,name="conv2wb_77"))

      conb00 = tf.concat(axis = 3, values = [self.images,self.images_wb])
      conv_wb9 = tf.nn.relu(conv2d(conb00, 3,32, k_h=7, k_w=7, d_h=1, d_w=1,name="conv2wb_9"))
      conv_wb10 = tf.nn.relu(conv2d(conv_wb9, 32,32, k_h=5, k_w=5, d_h=1, d_w=1,name="conv2wb_10"))
      wb1 =tf.nn.relu(conv2d(conv_wb10, 32,3, k_h=3, k_w=3, d_h=1, d_w=1,name="conv2wb_11"))

      conb11 = tf.concat(axis = 3, values = [self.images,self.images_ce])
      conv_wb99 = tf.nn.relu(conv2d(conb11, 3,32, k_h=7, k_w=7, d_h=1, d_w=1,name="conv2wb_99"))
      conv_wb100 = tf.nn.relu(conv2d(conv_wb99, 32,32, k_h=5, k_w=5, d_h=1, d_w=1,name="conv2wb_100"))
      ce1 =tf.nn.relu(conv2d(conv_wb100, 32,3, k_h=3, k_w=3, d_h=1, d_w=1,name="conv2wb_111"))

      conb111 = tf.concat(axis = 3, values = [self.images,self.images_gc])
      conv_wb999 = tf.nn.relu(conv2d(conb111, 3,32, k_h=7, k_w=7, d_h=1, d_w=1,name="conv2wb_999"))
      conv_wb1000 = tf.nn.relu(conv2d(conv_wb999, 32,32, k_h=5, k_w=5, d_h=1, d_w=1,name="conv2wb_1000"))
      gc1 =tf.nn.relu(conv2d(conv_wb1000, 32,3, k_h=3, k_w=3, d_h=1, d_w=1,name="conv2wb_1111"))

      weight_wb,weight_ce,weight_gc=tf.split(conv_wb77,3,3)
      output1=tf.add(tf.add(tf.multiply(wb1,weight_wb),tf.multiply(ce1,weight_ce)),tf.multiply(gc1,weight_gc))

    return output1


  def save(self, checkpoint_dir, step):
    model_name = "coarse.model"
    model_dir = "%s_%s" % ("coarse", self.label_height)
    checkpoint_dir = os.path.join(checkpoint_dir, model_dir)

    if not os.path.exists(checkpoint_dir):
        os.makedirs(checkpoint_dir)

    self.saver.save(self.sess,
                    os.path.join(checkpoint_dir, model_name),
                    global_step=step)

  def load(self, checkpoint_dir):
    print(" [*] Reading checkpoints...")
    # 固定使用 coarse_112 目录，而不是根据 label_height 动态生成
    model_dir = "coarse_112"
    checkpoint_dir = os.path.join(checkpoint_dir, model_dir)

    ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
    if ckpt and ckpt.model_checkpoint_path:
        ckpt_name = os.path.basename(ckpt.model_checkpoint_path)
        print(f"Found checkpoint: {ckpt_name} in {checkpoint_dir}")
        self.saver.restore(self.sess, os.path.join(checkpoint_dir, ckpt_name))
        return True
    else:
        print(f"No checkpoint found in {checkpoint_dir}")
        return False

