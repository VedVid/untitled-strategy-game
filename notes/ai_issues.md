AI uses pathfinder to find path from source (Enemy) to potential target (Player, MapObject).

Looks like it can find path from Enemy to Player, but not from Enemy to MapObject because MapObject blocks? But player blocks too?... Not sure how it works.

Anyway, there is a prototype AI in works, and there are several issues about that. Please see below.

![alt text](E:\programming\python\projects\strategy\notes\fig4.png)

```
enemy at 0, 1 acts...
    priority: 3,   obj: <game.being.Player object at 0x000002056E7FC7C0>  at  0, 0
enemy at 3, 5 acts...
    priority: 6,   obj: <game.map_object.MapObject object at 0x000002056E8247C0>  at  5, 5
    priority: 4,   obj: <game.map_object.MapObject object at 0x000002056E828340>  at  3, 7
    priority: 2,   obj: <game.being.Player object at 0x000002056E7F4490>  at  2, 4
enemy at 4, 1 acts...
    priority: 3,   obj: <game.map_object.MapObject object at 0x000002056E8247C0>  at  5, 5
enemy at 2, 1 acts...
    priority: 7,   obj: <game.map_object.MapObject object at 0x000002056E81DF10>  at  2, 0
    priority: 1,   obj: <game.being.Player object at 0x000002056E7FC7C0>  at  0, 0
    priority: 1,   obj: <game.being.Player object at 0x000002056E7F4490>  at  2, 4
```

Problems:
1. With range==5, enemy 1 should be able to target, in addition to entities already in list: player at (2, 4)
2. Enemy 2 should be able to target city at (6, 4), player at (7, 3). Range is one tile too short - it doesn't take into account that first element of path is under the Enemy?
3. Enemy 3 finds only city at (5, 5), and doesn't even take into account city at (2, 0) that is much closer. It should also find: city at (6, 4), player at (7, 3), player at (2, 4). Does take into account tile under player?
4. Enemy 4 find city at (2, 0), but also player at (0, 0) that is blocked by another Enemy - issue with pathfinding I guess? Maybe most of edge cases for player movement is handled by SpriteTracker instead of Pathfinding...

Potential causes:
1. Enemy Pathfinding works differently than Player pathfinding? When playing, Player can't go over Enemy, and Tiles that are <= Player.range are highlighted, and in Game when player tries to move_to position, it first tries to move to `Pathfinder.last_path[-Player.range]` (but from reverse, the first / last element is -1 and 0, hm...)
