  File "E:\programming\python\projects\strategy\game\grid.py", line 97, in generate_map
    self.generate_map()
  [Previous line repeated 64 more times]
  File "E:\programming\python\projects\strategy\game\grid.py", line 95, in generate_map
    if not self.check_map():
  File "E:\programming\python\projects\strategy\game\grid.py", line 165, in check_map
    pathfinder.clean_up_path_grid()
  File "E:\programming\python\projects\strategy\game\pathfinding.py", line 88, in clean_up_path_grid
    self._path_grid.cleanup()
AttributeError: 'NoneType' object has no attribute 'cleanup'

Process finished with exit code 1

