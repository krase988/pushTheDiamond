import tkinter as tk
import random
from tkinter import messagebox

# 실패 메시지 리스트
FAIL_MESSAGES = [
    "Failure.", "You failed.", "Mission failed.", "Try again.", "Not quite.", "You lose.", "Game over.", "Defeated.", "Unsuccessful.", "Task failed.",
    "The path is closed.", "Your journey ends here.", "The gods are not with you.", "The world has turned against you.", "You have been bested.", "A hero's fall.", "The shadow claims you.", "Your light has faded.", "A bitter defeat.", "There is no redemption.", "Ouch! That hurt.",
    "You fell down.", "Oops, you messed up.", "Not this time, buddy.", "Did you even try?", "Better luck next time.", "Whoopsie-daisy!", "You're a natural... at failing.", "Look at you go! (Straight to the fail screen.)", "Who needs to win, anyway?", "Dead end.",
    "Error.", "End.", "Stop.", "Gone.", "Ruined.", "Over.", "Canceled.", "Broken.", "Lost.", "What went wrong?", "Did you even try?", "Are you sure about that?", "Where did you go?", "Whoops, wrong way?", "Did you forget something?", "Are you okay?", "What happened?", "Is this your best?", "Why did you stop?", "The ancient seal remains unbroken.", "The prophecy was wrong about you.", "The king falls.", "The last hope is gone.", "The gears of fate have stopped.", "History will not remember this moment.", "Your legend ends now.", "The kingdom mourns your loss.", "The prophecy remains unfulfilled.", "The curse holds strong.", "Nice try.", "You call that a plan?", "Pathetic.", "Don't quit your day job.", "I've seen better.", "Is that all you've got?", "A valiant effort... not.", "So close, yet so far.", "You're not going to make it.", "Seriously?", "You've disappointed me.", "You let everyone down.", "There is no hope left.", "The darkness wins.", "A sad end.", "All that effort... for nothing.", "You couldn't save them.", "The pain is unbearable.", "You are alone now.", "Your last breath.", "Every end is a new beginning.", "Failure is a part of the journey.", "To fail is to learn.", "The true challenge is in rising again.", "What defines you is how you get back up.", "A story with a sad ending.", "Not all battles are won.", "The lesson is in the loss.", "The path of a true hero is paved with defeat.", "This is not your time.", "Busted.", "Whiffed.", "Poof.", "Snapped.", "Wrecked.", "Miss.", "D'oh!", "Fumble.", "Fizzle.", "Nope."
]

LEVELS = ["START", "LEVEL1", "LEVEL2", "LEVEL3", "LEVEL4", "LEVEL5", "LEVELX", "YOUBEST"]

class PushTheDiamond:
    def __init__(self, root):
        self.root = root
        self.root.title("Push The Diamond")
        self.level = 0
        self.buttons = {}  # id: button
        self.button_names = {}  # id: name
        self.disabled = set()
        self.hint_label = None
        self.hint_text = ""
        self.success_func = None
        self.next_level = None
        self.diamond_id = None
        self.diamond_count = 0
        self.just_came_from_best = False
        self.create_widgets()
        self.goto_level(0)

    def start_firework(self):
        import random
        self._firework_active = True
        self._firework_items = []
        self._firework_count = 0
        self._max_firework = 30  # 폭죽 횟수
        self._firework()

    def stop_firework(self):
        self._firework_active = False
        # 폭죽 잔상 제거
        if hasattr(self, '_firework_items'):
            for item in self._firework_items:
                self.canvas.delete(item)
            self._firework_items.clear()

    def _firework(self):
        import random
        if not getattr(self, '_firework_active', False):
            return
        # 랜덤 위치, 랜덤 색상, 랜덤 크기 원 그리기
        x = random.randint(150, 850)
        y = random.randint(150, 700)
        r = random.randint(20, 60)
        color = random.choice(["red","orange","yellow","green","blue","purple","magenta","cyan","lime","gold","pink"])
        item = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="white", width=3)
        self._firework_items.append(item)
        # 잠시 후 원 삭제
        self.root.after(400, lambda i=item: self.canvas.delete(i))
        self._firework_count += 1
        if self._firework_count < self._max_firework:
            self.root.after(120, self._firework)
        else:
            self._firework_active = False


    def remove_levelx_timer(self):
        # Level X 타이머 라벨 및 타이머 제거
        if hasattr(self, 'levelx_timer_label') and self.levelx_timer_label:
            self.levelx_timer_label.destroy()
            self.levelx_timer_label = None
        self.levelx_timer_running = False
    def start_levelx_timer(self):
        self.levelx_timer_running = True
        self.levelx_start_time = self.root.winfo_toplevel().tk.call('after', 'info')
        self.levelx_timer_base = self.root.tk.call('after', 'info')
        self.levelx_timer_start = self.root.tk.call('after', 'info')
        self.levelx_timer_start = self.root.tk.call('after', 'info')
        import time
        self.levelx_timer_start = time.perf_counter()
        self.update_levelx_timer()

    def stop_levelx_timer(self):
        self.levelx_timer_running = False

    def update_levelx_timer(self):
        if not getattr(self, 'levelx_timer_running', False):
            return
        import time
        elapsed = time.perf_counter() - self.levelx_timer_start
        sec = int(elapsed)
        centi = int((elapsed - sec) * 100)
        timer_str = f"{sec:02d}:{centi:02d}"
        if hasattr(self, 'levelx_timer_label') and self.levelx_timer_label:
            self.levelx_timer_label.config(text=timer_str)
        self.root.after(10, self.update_levelx_timer)

    def add_missing_buttons(self):
        """
        ID 1~25 중 self.buttons에 없는 버튼을 찾아 즉시 생성해줍니다.
        """
        x_margin = 100
        y_margin = 100
        for btn_id in range(1, 26):
            if btn_id not in self.buttons:
                i = (btn_id-1)//5
                j = (btn_id-1)%5
                x = x_margin + j*150
                y = y_margin + i*150
                btn = tk.Button(self.root, text="", width=8, height=4, command=lambda i=btn_id: self.on_button(i), state=tk.NORMAL)
                self.buttons[btn_id] = btn
                win_id = self.canvas.create_window(x, y, window=btn, width=100, height=100)
                self.button_windows[btn_id] = win_id

    def debug_check_button_ids(self):
        """
        모든 버튼에 대해 눌렀을 때 btn_id가 정상적으로 출력되는지 확인하고,
        출력이 안되는 버튼이 있으면 강제로 출력되도록 command를 재설정한다.
        """
        def make_command(i):
            return lambda: print(f"btn_id: {i}")
        for btn_id in range(1, 28):
            btn = self.buttons.get(btn_id)
            if btn:
                # 기존 command를 임시로 print로 덮어씌움
                btn.config(command=make_command(btn_id))

    def restore_button_commands(self):
        """
        버튼의 command를 원래대로 on_button(btn_id)로 복구한다.
        """
        for btn_id in range(1, 28):
            btn = self.buttons.get(btn_id)
            if btn:
                btn.config(command=lambda i=btn_id: self.on_button(i))

    def remove_merged_buttons(self):
        # 캔버스에 있는 모든 윈도우 아이템 중 width=250인 것(합쳐진 버튼)을 삭제
        for item in self.canvas.find_all():
            if self.canvas.type(item) == 'window':
                try:
                    w = self.canvas.itemcget(item, 'width')
                    if w and int(float(w)) == 250:
                        self.canvas.delete(item)
                except:
                    pass

    def remove_all_buttons(self):
        # 모든 버튼을 캔버스에서 제거
        for btn_id, win_id in list(self.button_windows.items()):
            self.canvas.delete(win_id)
        self.buttons.clear()
        self.button_windows.clear()

    def create_two_buttons(self):
        # ID 26, 27번 버튼 생성
        x_margin = 100
        y_margin = 100
        self.buttons[26] = tk.Button(self.root, text="Hint", width=8, height=4, command=self.show_hint)
        win_id_26 = self.canvas.create_window(x_margin+5*150+75, y_margin+3*150, window=self.buttons[26], width=100, height=100)
        self.button_windows[26] = win_id_26
        self.buttons[27] = tk.Button(self.root, text="Exit", width=8, height=4, command=self.confirm_exit)
        win_id_27 = self.canvas.create_window(x_margin+5*150+75, y_margin+4*150, window=self.buttons[27], width=100, height=100)
        self.button_windows[27] = win_id_27

    def create_all_buttons(self):
        # ID 1~27까지 버튼 딕셔너리와 윈도우 딕셔너리 초기화
        self.buttons = {}
        self.button_windows = {}
        # 1~25번 버튼(5x5) + 26,27번 버튼 생성
        x_margin = 100
        y_margin = 100
        for i in range(5):
            for j in range(5):
                btn_id = i*5 + j + 1
                x = x_margin + j*150
                y = y_margin + i*150
                btn = tk.Button(self.root, text="", width=8, height=4, command=lambda i=btn_id: self.on_button(i))
                self.buttons[btn_id] = btn
                win_id = self.canvas.create_window(x, y, window=btn, width=100, height=100)
                self.button_windows[btn_id] = win_id
        # 우측 하단 버튼 2개
        self.create_two_buttons()
        
    def create_widgets(self):
        self.root.geometry("1000x800")
        self.canvas = tk.Canvas(self.root, width=1000, height=800, bg="white")
        self.canvas.pack()
        # 버튼 생성 (중복 제거, 함수로 위임)
        self.create_all_buttons()
        # 세로 검은 선
        x_margin = 100
        y_margin = 100
        self.canvas.create_line(x_margin+5*150+1, y_margin, x_margin+5*150+1, y_margin+5*150, fill="black", width=2)
        # 힌트 라벨
        self.hint_label = tk.Label(self.root, text="", font=("Arial", 16), fg="blue")
        self.canvas.create_window(475, 20, window=self.hint_label)

    def confirm_exit(self):
        if messagebox.askyesno("Exit", "정말 종료하시겠습니까?"):
            self.root.quit()

    def reset_buttons(self):
        for i in range(1, 28):
            btn = self.buttons.get(i)
            if btn:
                btn.config(text="", state=tk.NORMAL, bg="SystemButtonFace")
        self.disabled.clear()
        self.button_names.clear()
        self.diamond_id = None

    def reset_buttons_25(self):
        for i in range(1, 26):
            btn = self.buttons.get(i)
            if btn:
                btn.config(text="", state=tk.NORMAL, bg="SystemButtonFace")
        self.disabled.clear()
        self.button_names.clear()
        self.diamond_id = None

    def set_button_name(self, btn_id, name, disable=False):
        btn = self.buttons.get(btn_id)
        if btn:
            btn.config(text=name)
            self.button_names[btn_id] = name
            if disable:
                btn.config(state=tk.DISABLED)
                self.disabled.add(btn_id)
            else:
                btn.config(state=tk.NORMAL)
                self.disabled.discard(btn_id)

    def on_button(self, btn_id):
        if btn_id in self.disabled:
            return
        if self.success_func:
            self.success_func(btn_id)

    def show_hint(self):
        if self.hint_text:
            self.hint_label.config(text=self.hint_text)
            # 5초 후 힌트 메시지 자동 삭제
            self.hint_label.after(3000, lambda: self.hint_label.config(text=""))

    def fail(self):
        msg = random.choice(FAIL_MESSAGES)
        messagebox.showinfo("Fail", msg)
        self.goto_level(self.level)

    def fail_level4(self):
        msg = random.choice(FAIL_MESSAGES)
        messagebox.showinfo("Fail", msg)
        #self.remove_all_buttons()
        #self.create_all_buttons()
        self.add_missing_buttons()
        self.reset_buttons()
        self.remove_merged_buttons()
        self.restore_button_commands()
        self.create_two_buttons()
        self.level4()

    def goto_level(self, level):
        self.level = level
        self.reset_buttons()
        self.hint_label.config(text="")
        # 항상 26=Hint, 27=Exit로 세팅 (별도 표기 있을 때만 예외)
        if level != 0:
            self.set_button_name(26, "Hint")
            self.set_button_name(27, "Exit")
        # 레벨 안내 메시지
        level_names = [
            "START", "LEVEL 1", "LEVEL 2", "LEVEL 3", "LEVEL 4", "LEVEL 5", "LEVEL X", "YOU BEST"
        ]
        if 0 < level < len(level_names):
            messagebox.showinfo("LEVEL", f"{level_names[level]}")
        if level == 0:
            self.level_start()
        elif level == 1:
            self.level1()
        elif level == 2:
            self.level2()
        elif level == 3:
            self.level3()
        elif level == 4:
            self.level4()
        elif level == 5:
            self.level5()
        elif level == 6:
            self.levelx()
        elif level == 7:
            self.level_best()

    # 시작 화면
    def level_start(self):
        self.hint_text = "Push The Diamond에 오신 것을 환영합니다!"
        self.remove_levelx_timer()
        self.set_button_name(7, "Push")
        self.set_button_name(8, "the")
        self.set_button_name(9, "Diamond")
        self.set_button_name(13, "Start")
        self.set_button_name(18, "Exit")
        self.set_button_name(26, "Developer")
        self.set_button_name(27, "DWSHIN")
        # YOUR BEST에서 돌아온 경우 23번 버튼에 특수 기능 부여
        if self.just_came_from_best:
            self.set_button_name(23, "Go Level X")
        else:
            self.set_button_name(23, "")
        def start_func(btn_id):
            if btn_id == 13:
                self.goto_level(1)
            elif btn_id == 18:
                self.root.quit()
            elif btn_id == 23 and self.just_came_from_best:
                self.just_came_from_best = False
                self.goto_level(6)
        self.success_func = start_func

    # Level 1
    def level1(self):
        self.hint_text = "시작이자 끝"
        diamond = random.randint(1, 25)
        self.set_button_name(diamond, "◆")
        self.diamond_id = diamond
        def func(btn_id):
            if btn_id == self.diamond_id:
                self.goto_level(2)
            else:
                self.fail()
        self.success_func = func

    # Level 2
    def level2(self):
        self.hint_text = "네 손으로 떠받치기"
        candidates = [7,8,9,12,13,14,17,18,19]
        diamond = random.choice(candidates)
        self.set_button_name(diamond, "◆", disable=True)
        self.diamond_id = diamond
        self.activated = set()
        def func(btn_id):
            if btn_id == self.diamond_id:
                # 네 방향을 모두 누른 후에만 ◆ 버튼이 활성화됨
                if self.buttons[btn_id]['state'] == tk.NORMAL:
                    self.goto_level(3)
                # 네 방향을 모두 누르기 전에는 아무 일도 일어나지 않음
                return
            # 네 방향 체크 (중복 방지)
            adj = self.get_adjacent(self.diamond_id)
            if btn_id in adj and btn_id not in self.activated:
                self.activated.add(btn_id)
                if len(self.activated) == 4:
                    self.set_button_name(self.diamond_id, "◆", disable=False)
                    self.buttons[self.diamond_id].update_idletasks()
            elif btn_id not in adj:
                self.fail()
        self.success_func = func

    def get_adjacent(self, btn_id):
        # 5x5 그리드에서 상하좌우
        adj = []
        row = (btn_id-1)//5
        col = (btn_id-1)%5
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = row+dr, col+dc
            if 0<=nr<5 and 0<=nc<5:
                adj.append(nr*5+nc+1)
        return adj

    # Level 3
    def level3(self):
        self.hint_text = "두 눈 크게 뜨고"
        names = ["!", "@", "#", "$", "%", "^", "&", "*", ";", ":", "?", "/", "_", "+", "☆", "※", "★", "♠", "♣", "◎", "◇", "◆", "□", "■", "♥"]
        btn_ids = list(range(1, 26))
        random.shuffle(btn_ids)
        for btn_id, name in zip(btn_ids, names):
            self.set_button_name(btn_id, name)
        # ◆가 할당된 버튼 id 찾기
        for btn_id in btn_ids:
            if self.buttons[btn_id]['text'] == "◆":
                self.diamond_id = btn_id
                break
        def func(btn_id):
            if btn_id == self.diamond_id:
                self.goto_level(4)
            else:
                self.fail()
        self.success_func = func

    # Level 4
    def level4(self):
        self.hint_text = "십시일반"
        lefts = [7,8,12,13,17,18]
        left = random.choice(lefts)
        right = left+1
        self.set_button_name(left, "◀", disable=True)
        self.set_button_name(right, "▶", disable=True)
        # 합쳐질 버튼의 주변 id
        merge_ids = [left-6, left-5, left-4, left-3, left-1, left+2, left+4, left+5, left+6, left+7]
        pressed = set()
        merged = [False]
        def func(btn_id):
            #print(f"Button pressed: {btn_id}, Merged: {merged[0]}")
            if not merged[0]:
                if btn_id in merge_ids:
                    pressed.add(btn_id)
                    #print(f"Pressed: {pressed}, Btn IDs: {btn_id}")
                    if len(pressed) == len(merge_ids):
                        # self.buttons에서 left, right 항목을 삭제  
                        # 합치기: 삭제 전 ◀/▶ 버튼을 활성화(NORMAL)로 변경
                        if left in self.buttons:
                            self.buttons[left].config(state=tk.NORMAL)  
                        if right in self.buttons:
                            self.buttons[right].config(state=tk.NORMAL) 
                        # self.buttons에서 left, right 항목을 삭제
                        if left in self.buttons:
                            del self.buttons[left]  
                        if right in self.buttons:
                            del self.buttons[right] 
                        # 캔버스에서 기존 버튼 제거
                        self.canvas.delete(self.button_windows[left])
                        self.canvas.delete(self.button_windows[right])
                        # big_btn 위치를 ◀ 버튼이 있던 위치에 생성
                        coords = self.canvas.coords(self.button_windows[left])
                        if coords:
                            x, y = coords[0], coords[1]
                        else:
                            x_margin = 100
                            y_margin = 100
                            row = (left-1)//5
                            col = (left-1)%5
                            x = x_margin + col*150
                            y = y_margin + row*150
                        # big_btn 생성 및 참조 저장
                        self.big_btn_id = None
                        def big_btn_command():
                            self.goto_level(5)
                        big_btn = tk.Button(self.root, text="◆", width=20, height=4, command=big_btn_command)
                        self.big_btn_id = self.canvas.create_window(x + 75, y, window=big_btn, width=250, height=100)
                        merged[0] = True
                else:
                    self.fail_level4()
            else:
                self.fail_level4()
        self.success_func = func

    # Level 5
    def level5(self):
        # 모든 버튼을 삭제 후 다시 생성
        self.remove_all_buttons()
        self.create_all_buttons()
        self.remove_merged_buttons()
        self.hint_text = "끝이자 시작"
        targets = [3,7,8,9,11,12,13,14,15,17,18,19,23]
        pressed = set()
        def func(btn_id):
            if btn_id in targets:
                pressed.add(btn_id)
                if len(pressed) == len(targets):
                    self.goto_level(6)
            else:
                self.fail()
        self.success_func = func

    # Level X
    def levelx(self):
        self.hint_text = "축하합니다! 성공했어요!10"
        self.set_button_name(1, "축")
        self.set_button_name(2, "하")
        self.set_button_name(3, "합")
        self.set_button_name(4, "니")
        self.set_button_name(5, "다")
        self.set_button_name(21, "성")
        self.set_button_name(22, "공")
        self.set_button_name(23, "했")
        self.set_button_name(24, "어")
        self.set_button_name(25, "요")
        self.diamond_count = 0
        # 타이머 라벨 생성 (우측 상단)
        if hasattr(self, 'levelx_timer_label') and self.levelx_timer_label:
            self.levelx_timer_label.destroy()
        self.levelx_timer_label = tk.Label(self.root, text="00:00", font=("Arial", 18), fg="red", bg="white")
        self.canvas.create_window(900, 40, window=self.levelx_timer_label)
        self.levelx_timer_running = False
        def set_random_diamond():
            for i in range(6, 21):
                self.set_button_name(i, "")
            diamond = random.randint(6, 20)
            self.set_button_name(diamond, "◆")
            self.diamond_id = diamond
        set_random_diamond()
        def func(btn_id):
            if btn_id == self.diamond_id:
                if self.diamond_count == 0:
                    self.start_levelx_timer()
                self.diamond_count += 1
                if self.diamond_count == 10:
                    self.stop_levelx_timer()
                    self.goto_level(7)
                else:
                    set_random_diamond()
            else:
                self.fail()
        self.success_func = func

    # YOU BEST
    def level_best(self):
        self.hint_text = "YOU BEST!"
        self.set_button_name(13, "BEST!")
        self.set_button_name(25, "HOME")
        self.start_firework()
        def func(btn_id):
            if btn_id == 25:
                self.stop_firework()
                self.just_came_from_best = True
                self.goto_level(0)
        self.success_func = func

if __name__ == "__main__":
    root = tk.Tk()
    app = PushTheDiamond(root)
    root.mainloop()
