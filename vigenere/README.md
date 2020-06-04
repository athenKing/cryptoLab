## Features

* Combine fixed constant friedmantest and Kaisisktest to identify the possible keylength

With a cipher_len/key_len ration around one houndred, the Kaisisktest will most possibly discern the key length

* The key is derived by calculating the possible caesar key shift regarding natural english frequency(such as very low apperances of x,y and high frequency of e,a)


## Engineering spotlights

Uses powerful SortQueue structure to store the elements in decreasing or increasing order with fixed size.

It contains a whole range search algorithm(Even though it's dumb)

It contains some cache room for trying different keyLength and different key Combinations.  