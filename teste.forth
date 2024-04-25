: EGGSIZE
   dup 18 < if  ." reject "      else
   dup 21 < if  ." small "       else
   dup 24 < if  ." medium "      else
   dup 27 < if  ." large "       else
   dup 30 < if  ." extra large " else
      ." error "
   then then then then then drop ;

25 EGGSIZE
