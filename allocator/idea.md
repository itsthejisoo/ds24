## 해시테이블을 사용하여 allocator를 구현한 이유


### 배열
- 장점<br>
  - free할 메모리 id를 조회하는데 O(1) 시간이 걸린다.
- 단점<br>
    - 삽입과 삭제 모두 시간복잡도가 O(n)이다.


### 연결리스트
- 장점<br>
    - 삽입과 삭제 모두 시간복잡도가 O(1)이다.<br>
    - chunk의 크기는 정해져있지만, 노드의 크기를 동적으로 조정할 수 있다. -> 사용 중인 메모리 크기 계산하기 수월
- 단점<br>
    - free할 메모리 id를 조회하는데 O(n)의 시간이 걸린다.<br>
    - 포인터 오버헤드가 있다.


### 이진트리
- 장점<br>
    - 탐색의 시간복잡도가 O(logn)이다.<br>
    - 메모리 풀의 크기가 커져서 효율적
- 단점<br>
    - 트리의 균형을 유지하기 위해서 복잡해진다.

### 해시테이블
- 장점<br>
    - 메모리 할당, 해제에서 시간 복잡도 O(1)이다.
- 단점<br>
    - 할당 요청이 많지 않은 경우 해시 테이블의 공간 활용 효율성이 떨어진다. - 메모리 오버헤드

### chained 해시테이블
- 장점<br>
    - 삽입, 삭제, 탐색이 평균적으로 O(1)의 시간복잡도를 지닌다.
    - 동적 할당 가능하고 요청한 크기만큼의 메모리를 할당할 수 있어서 메모리 공간을 효율적으로 쓸 수 있다.
- 단점<br>
    - 포인터 오버헤드
    - 사용하지 않는 메모리 공간 낭비

#### 처음에 사용해본 자료구조 : chained hash table
- chained hash table을 고른 이유:
    한 id에 청크가 무조건 1개가 아니므로 연결리스트로 같은 식별번호끼리 연결해줘야함. → 연결리스트 필수 <br>
    해시 테이블은 삽입, 삭제, id 탐색할 때 시간 복잡도가 O(1)이므로 좋은 성능을 보인다. <br>
    하지만 연결리스트를 사용한 이상 어쩔 수 없이 탐색에서 O(n) 시간이 소요된다. 따라서 chained hash table은 malloc과 free 둘 다 O(n)의 시간이 걸림 -> 최선의 방법은 아닌 것 같음<br>
    참고) index를 id로 하면 충돌이 일어나는 것을 방지할 수 있다.<br>
    <br>

#### 두번째로 생각해본 자료구조 : 딕셔너리로 메모리를 할당하고, chunk가 두 개일 경우에 배열로 할당해주기
- malloc 함수:<br> chunk가 여러 개일 경우 할당할때 배열에 chunk의 개수만큼 삽입해야하므로 O(n)이 걸림
- free 함수: <br> 키 존재 여부를 확인하고 삭제하는데 O(1)의 시간이 걸림