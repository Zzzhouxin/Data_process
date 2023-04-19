##### get_puredata.py

按照IP + banner_list + product的格式储存为新的pure_data
输出：pure_data，json

##### reduce_bannerlist.py

筛选我们需要的深度探索特征，去掉其他无用的数据字段
输出：train_text.json

###### Take_apart_bannerlist.py

把每个bannerlist里的数据，根据正则表达式拆解成状态码，关键字，body字段三部分
输出：train_text2.json

###### remove_html_label.py

将一些时间类型的数据写成通用宏定义,去除part3中的html有关标签	# 还需要修改
输出：train_text3.json

###### get_train_data.py

生成所需格式的训练数据

###### sim_hash.py

用sim_hash对样本去重

