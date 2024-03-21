import copy

# 퍼즐 사이즈
size_col = 3
size_row = 3
# 연산자 명
op_none_root = 0
op_up = 1
op_left = 2
op_down = 3
op_right = 4
# 연산자 이름 리스트
list_op: list[str] = [
    "ROOT", "UP", "LEFT", "DOWN", "RIGHT"
]


# 노드 클래스
class Node:
    # 퍼즐의 상태, g(n)의 값, 이 상태로 오기 직전의 연산자
    def __init__(self, state: list[int], score_g: int, operation: int):
        self.state = state
        self.score_g = score_g
        self.operation = operation

    # 퍼즐 디스플레이
    def display(self):
        print(f'last operation: {list_op[self.operation]}')
        for i in range(size_row):
            temp: list[int] = []
            for j in range(size_col):
                temp.append(self.state[i * size_col + j])
            print(temp)


# 노드와 두 인덱스를 입력받아 노드 상태의 해당 인덱스의 값을 서로 바꾸고, 바뀐 노드를 반환하는 함수
def create_node(parent: Node, index_target: int, cursor: int, score_g: int, operation: int) -> Node:
    # index_target과 cursor 위치의 값을 서로 바꾸기
    list_temp = copy.deepcopy(parent.state)
    value_temp = list_temp[cursor]
    list_temp[cursor] = 0
    list_temp[index_target] = value_temp
    # 바뀌어진 상태를 기반으로 노드 생성
    return Node(list_temp, score_g, operation)


# 입력받은 노드가 opened, closed 리스트의 노드 중에 중복하여 존재하는지 확인하는 함수
def is_node_duplicate(node, list_node):
    for i in list_node:
        if i.state == node.state:
            return True
    return False


# 노드를 입력받으면 그 노드의 자식들을 가능한 만큼 생성하여 반환하는 함수
def create_child(parent: Node, score_g: int, list_node: list[Node]) -> list[Node]:
    index_target = parent.state.index(0)
    list_result: list[Node] = []
    # UP 연산자
    if index_target >= size_col:
        node_up = create_node(parent, index_target, index_target - size_col, score_g, op_up)
        if not is_node_duplicate(node_up, list_node):
            list_result.append(node_up)
    # LEFT 연산자
    if not index_target % size_col == 0:
        node_left = create_node(parent, index_target, index_target - 1, score_g, op_left)
        if not is_node_duplicate(node_left, list_node):
            list_result.append(node_left)
    # DOWN 연산자
    if index_target < (size_row * size_col) - size_col:
        node_down = create_node(parent, index_target, index_target + size_col, score_g, op_down)
        if not is_node_duplicate(node_down, list_node):
            list_result.append(node_down)
    # RIGHT 연산자
    if not index_target % size_col == size_col - 1:
        node_right = create_node(parent, index_target, index_target + 1, score_g, op_right)
        if not is_node_duplicate(node_right, list_node):
            list_result.append(node_right)
    return list_result


# h(n) 평가 함수
def get_h(state_current: list[int], state_obj: list[int]):
    if state_current == state_obj:
        return 0
    else:
        h: int = 0
        for i in range(len(state_current)):
            if state_current[i] != state_obj[i]:
                h += 1
        return h


# A* 탐색 함수
# 기본 상태와 목표 상태를 입력받아서 탐색 과정을 표시한다.
def a_star_search(state_init: list[int], state_obj: list[int]):
    score_g: int = 0
    # opened 노드의 리스트, 기본 값으로 루트 노드를 부여한다.
    list_opened: list[Node] = [Node(state_init, score_g, op_none_root)]
    # 확인이 끝난 리스트
    list_closed: list[Node] = []
    while True:
        # 확인이 필요한 리스트가 더 없으면 순회를 종료한다.
        if not list_opened:
            print("solution not found.\n\n")
            break
        # opened 리스트의 노드들을 f(n) 평가한다.
        list_f: list[int] = []
        for i in list_opened:
            score_h = get_h(i.state, state_obj)
            list_f.append(i.score_g + score_h)
        index_min = list_f.index(min(list_f))
        # 가장 f(n) 점수가 낮은 노드를 선택한다.
        selected = list_opened[index_min]
        # 선택된 노드가 이전에 만들어진 노드면
        if selected.score_g != score_g:
            print("back to parent.")
        # 노드의 상태를 이차원 배열로 표시한다.
        selected.display()
        print(f"f(n) = {min(list_f)} = g(n) + h(n) = {selected.score_g} + {min(list_f) - selected.score_g}")
        print()
        # 현재 노드가 목표 노드와 같으면 순회를 종료한다.
        if selected.state == state_obj:
            print("solution found.\n\n")
            break
        # 같지 않으면 g(n) 값을 증가시킨다.
        score_g += 1
        # 현재 노드의 자식 노드들을 생성하고 opened 리스트에 추가한다.
        list_opened += create_child(selected, score_g, list_opened + list_closed)
        # 현재 노드를 closed 리스트에 추가한다.
        list_closed.append(list_opened.pop(index_min))


if __name__ == "__main__":
    a_star_search([1, 3, 0, 4, 2, 5, 7, 8, 6], [1, 2, 3, 4, 5, 6, 7, 8, 0])
    # a_star_search([0, 1, 3, 4, 2, 5, 7, 8, 6], [1, 2, 3, 4, 5, 6, 7, 8, 0])
    # a_star_search([1, 2, 3, 0, 4, 6, 7, 5, 8], [1, 2, 3, 4, 5, 6, 7, 8, 0])
    # a_star_search([2, 8, 3, 1, 6, 4, 7, 0, 5], [1, 2, 3, 8, 0, 4, 7, 6, 5])
