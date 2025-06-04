from ERP2XML import *
kg = KnowledgeGraph()

#以下内容仅为示例


#画布大小 0*0-5000*5000
#每个entity的大小 200*120

# 添加节点
# kg.add_entity(content, distinct_type, addon_types, x, y)
# 参数：
# - content：节点内容
# - distinct_type：独立实体类型，分别是 ka (知识领域)、ku (知识单元)、kp (知识点)、kd (知识细节)
# - addon_types：附加实体类型，为 k (知识)、t (思维)、e (示例)、q (问题)、p (练习)、z (思政) 的组合
# - x：横坐标
# - y：纵坐标
#
# 返回：节点 id
entity_1 = kg.add_entity("这里是节点一", "ku", "", 100.0, 100.0)
entity_2 = kg.add_entity("这里是节点二", "ku", "", 380.0, 100.0)

#连接节点1， 节点2
kg.add_edge(entity_1, entity_2, "order")


xml_str = kg.to_xml()
with open("output.xml", "w", encoding="utf-8") as f:
    f.write(xml_str)
print(xml_str)