python与redis旧版本数据库的交互：
zadd: db.zadd(REDIS_KEY, score, member)
zincrby: db.zincrby(REDIS_KEY, member, increment)

如果是在redis新版本中还使用上面的语句：将会分别出现下面的异常：
AttributeError: ‘int’ object has no attribute ‘items’
(error) ERR value is not a valid float

python与redis新版本数据库交互：
zadd：db.zadd(REDIS_KEY, {member:score})
zincrby：db.zincrby(REDIS_KEY, increment, menber)
