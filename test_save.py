import mazepy
mazepy.mazenav.random_seed()
mazepy.mazenav.initmaze("hard_maze_list.txt")
artifact_class=mazepy.arenaorg
new_art=artifact_class()
new_art.init_rand()
new_art.mutate()
new_art.save("out.txt")
