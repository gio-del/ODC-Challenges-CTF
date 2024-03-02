I think the problem is that the binary is setting the seed with the clock time but getting bytes that can be easily guessed

To solve this challenge we will let first the binary shuffle the asm then we send the shuffled assembly to the binary, probabily it will be deshuffled in the correct way