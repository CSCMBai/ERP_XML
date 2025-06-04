_DISTINCT_TYPE_MAP = {
    "ka": "知识领域",
    "ku": "知识单元",
    "kp": "知识点",
    "kd": "知识细节"
}
LEVEL = "归纳级"
CLASSIFICATION = "内容方法型节点"
IDENTITY = "知识"
OPENTOOL = "无"
ADDON_TYPE_ORDER = ['k', 't', 'e', 'q', 'p', 'z']

def escape_non_ascii(text):
    return ''.join(
        c if ord(c) < 128 else f'&#{ord(c)};'
        for c in str(text)
    )

def parse_addon_types(addon_types_str):
    return set(c for c in addon_types_str.lower() if c in ADDON_TYPE_ORDER)

def addon_types_to_attach_code(addon_types_set):
    return ''.join(['1' if c in addon_types_set else '0' for c in ADDON_TYPE_ORDER])

def relation_info(rel_type):
    if rel_type == "contain":
        return "包含", "包含关系", "包含关系"
    elif rel_type == "order":
        return "次序", "次序关系", "次序关系"
    else:
        return "未知", "未知关系", "未知关系"

class KnowledgeGraph:
    def __init__(self):
        self._nodes = {}
        self._edges = []
        self._id_counter = 1

    def add_entity(self, content, distinct_type, addon_types, x, y):
        node_id = self._id_counter
        self._nodes[node_id] = {
            "id": node_id,
            "class_name": _DISTINCT_TYPE_MAP.get(distinct_type, "未知类型"),
            "classification": CLASSIFICATION,
            "identity": IDENTITY,
            "level": LEVEL,
            "attach": addon_types_to_attach_code(parse_addon_types(addon_types)),
            "opentool": OPENTOOL,
            "content": content,
            "x": float(x),
            "y": float(y)
        }
        self._id_counter += 1
        return node_id

    def add_edge(self, from_id, to_id, rel_type):
        # rel_type: "contain" or "order"
        self._edges.append({
            "from": from_id,
            "to": to_id,
            "type": rel_type
        })

    def to_xml(self):
        tab = "\t"
        lines = []
        lines.append("<KG>")
        lines.append(f"{tab}{escape_non_ascii('教学知识图谱')}")
        lines.append(f"{tab}<entities>")
        for node in self._nodes.values():
            lines.append(f"{tab*2}<entity>")
            lines.append(f"{tab*3}<id>{node['id']}</id>")
            lines.append(f"{tab*3}<class_name>{escape_non_ascii(node['class_name'])}</class_name>")
            lines.append(f"{tab*3}<classification>{escape_non_ascii(node['classification'])}</classification>")
            lines.append(f"{tab*3}<identity>{escape_non_ascii(node['identity'])}</identity>")
            lines.append(f"{tab*3}<level>{escape_non_ascii(node['level'])}</level>")
            lines.append(f"{tab*3}<attach>{node['attach']}</attach>")
            lines.append(f"{tab*3}<opentool>{escape_non_ascii(node['opentool'])}</opentool>")
            lines.append(f"{tab*3}<content>{escape_non_ascii(node['content'])}</content>")
            lines.append(f"{tab*3}<x>{node['x']}</x>")
            lines.append(f"{tab*3}<y>{node['y']}</y>")
            lines.append(f"{tab*2}</entity>")
        lines.append(f"{tab}</entities>")
        if self._edges:
            lines.append(f"{tab}<relations>")
            for edge in self._edges:
                name, class_name, classification = relation_info(edge["type"])
                lines.append(f"{tab*2}<relation>")
                lines.append(f"{tab*3}<name>{escape_non_ascii(name)}</name>")
                lines.append(f"{tab*3}<headnodeid>{edge['from']}</headnodeid>")
                lines.append(f"{tab*3}<tailnodeid>{edge['to']}</tailnodeid>")
                lines.append(f"{tab*3}<class_name>{escape_non_ascii(class_name)}</class_name>")
                lines.append(f"{tab*3}<mask>{escape_non_ascii('知识连线')}</mask>")
                lines.append(f"{tab*3}<classification>{escape_non_ascii(classification)}</classification>")
                lines.append(f"{tab*3}<head_need>{escape_non_ascii(CLASSIFICATION)}</head_need>")
                lines.append(f"{tab*3}<tail_need>{escape_non_ascii(CLASSIFICATION)}</tail_need>")
                lines.append(f"{tab*2}</relation>")
            lines.append(f"{tab}</relations>")
        else:
            lines.append(f"{tab}<relations />")
        lines.append("</KG>")
        return "\n".join(lines)