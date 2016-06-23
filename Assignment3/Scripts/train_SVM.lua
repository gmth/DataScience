-- Plan B file

require('torch')
-- require the library to convert from Lua to Python
-- local py = require('fb.python')

features = torch.load('features.t7')

-- py.exec([=[
-- print(features)
-- ]=])

print(features)