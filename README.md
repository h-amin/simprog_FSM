# simprog_FSM
Creating a Finite State Machine simulation based off a simple game AI using python.

-------------------------------------------------[GENERAL FLOW]---------------------------------------------------------
1. mob is in IDLE state / mob is in w_route (walking route) state
2. system recognizes player within 15 m LoS range
3. mob approaches' player
4. mob enters 5m eval_range for evaluation
5. system evaluates player level in correspondence to mob level
6. system establishes mob lvl >= player lvl
7. mob approaches' player to initiate combat
8. player in 3 m ccmb_reach (combative reach), enter Combat state
9. mob attacks' player, vice versa
10. OPTION 1: mob hp down to 0, enter Defeat state
    OPTION 2: player hp down to 0, enter Victory state
-----------------------------------------------------[MISC]-------------------------------------------------------------
The program has been modelled in a specific way that does not allow the mob to enter a combat state when the enemy player
has a higher level than the mob itself. This is process that is handled by the EVALUATION state. Because the code relies
on levels to decide the result of combat, if the enemy player can never reach a higher level than the mob, in turn never
reach a defeat state. Throughout the build process of the program we came to the realisation that the original
FMA design had elements that are obsolete.
