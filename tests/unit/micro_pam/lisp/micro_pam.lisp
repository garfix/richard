(DE JUSTIFY (INPUT)
 (MSG T "Trying to explain")
 (SPRINT INPUT 4)
 (MSG T)
 (LOOP (INITIAL *CHAIN* NIL CD INPUT)
       (UNTIL (PREDICTED CD))
       (DO (MSG T "Does not confirm prediction" T)
           (PUSH (LIST CD *INFERENCE-RULES*) *CHAIN*))
       (WHILE (SETQ CD (TRY-INFERENCE))))
 (RESULT
  (COND (CD
         (MSG T "Adding inference chain to data base")
         (FOR (CD-INF IN (REVERSE *CHAIN*))
              (DO (UPDATE-DB (CAR CD-INF))))
         (UPDATE-DB CD))
        (T
         (MSG T "No inference chain found—adding")
         (UPDATE-DB INPUT)))))
