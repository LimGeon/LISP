(ATOM  X) ;  X가 ATOM(심볼)일 때만 참(true)를 반환함.
(NULL X) ;  X가 NIL일 때만 참(true)을 반환함.
(NUMBERP X) ;  X가 숫자일 때만 참(true)을 반환함.
(ZEROP X) ;  X가 0일 때만 참(true)을 반환함. X가 숫자가 아니면 ERROR 발생.
(MINUSP X) ; X가 음수일 때만 참(true)을 반환함. X가 숫자가 아니면 ERROR 발생.
(EQUAL X Y) ;  X와 Y가 같으면 참(true)을 반환함.
(< X Y) ;  X < Y 이면 참(true)을 반환함.
(>= X Y) ;  X >= Y 이면 참(true)을 반환함.
(STRINGP X) ;  X가 STRING일 때만 참(true)을 반환함.
(STRINGP "A")
(SETQ A "HI THERE")
(STRINGP A)
(STRINGP #\A) ;  문자
(STRINGP '(A B C)) ;  리스트
(STRINGP 1.2) ;  숫자
(STRINGP 'A) ;  심볼
(STRINGP #(0 1 2)) ;  배열
(STRINGP NIL)