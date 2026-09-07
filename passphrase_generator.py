import math
import secrets


# A curated list of 2048 common, easy-to-type English words
# (4-7 letters, filtered from a common-word frequency list).
# 2048 = 2^11, so each word picked from this list contributes
# exactly 11 bits of entropy -- easy to reason about and cite.
WORDLIST = [
    'that', 'this', 'with', 'from', 'your', 'have', 'more', 'will',
    'home', 'about', 'page', 'search', 'free', 'other', 'time', 'they',
    'site', 'what', 'which', 'their', 'news', 'there', 'only', 'when',
    'contact', 'here', 'also', 'help', 'view', 'online', 'first', 'been',
    'would', 'were', 'some', 'these', 'click', 'like', 'service', 'than',
    'find', 'price', 'date', 'back', 'people', 'list', 'name', 'just',
    'over', 'state', 'year', 'into', 'email', 'health', 'world', 'next',
    'used', 'work', 'last', 'most', 'music', 'data', 'make', 'them',
    'should', 'product', 'system', 'post', 'city', 'policy', 'number', 'such',
    'please', 'support', 'message', 'after', 'best', 'then', 'good', 'video',
    'well', 'where', 'info', 'rights', 'public', 'books', 'high', 'school',
    'through', 'each', 'links', 'review', 'years', 'order', 'very', 'privacy',
    'book', 'items', 'company', 'read', 'group', 'need', 'many', 'user',
    'said', 'does', 'under', 'general', 'january', 'mail', 'full', 'reviews',
    'program', 'life', 'know', 'games', 'days', 'part', 'could', 'great',
    'united', 'hotel', 'real', 'item', 'center', 'ebay', 'must', 'store',
    'travel', 'made', 'report', 'member', 'details', 'line', 'terms', 'before',
    'hotels', 'send', 'right', 'type', 'because', 'local', 'those', 'using',
    'results', 'office', 'design', 'take', 'posted', 'address', 'within', 'states',
    'area', 'want', 'phone', 'subject', 'between', 'forum', 'family', 'long',
    'based', 'code', 'show', 'even', 'black', 'check', 'special', 'prices',
    'website', 'index', 'being', 'women', 'much', 'sign', 'file', 'link',
    'open', 'today', 'south', 'case', 'project', 'same', 'pages', 'version',
    'section', 'found', 'sports', 'house', 'related', 'both', 'county', 'photo',
    'game', 'members', 'power', 'while', 'care', 'network', 'down', 'systems',
    'three', 'total', 'place', 'without', 'access', 'think', 'north', 'current',
    'posts', 'media', 'control', 'water', 'history', 'size', 'since', 'guide',
    'shop', 'board', 'change', 'white', 'text', 'small', 'rating', 'rate',
    'during', 'return', 'account', 'times', 'sites', 'level', 'digital', 'profile',
    'form', 'events', 'love', 'john', 'main', 'call', 'hours', 'image',
    'title', 'another', 'shall', 'class', 'still', 'money', 'quality', 'every',
    'listing', 'content', 'country', 'private', 'little', 'visit', 'save', 'tools',
    'reply', 'compare', 'movies', 'include', 'college', 'value', 'article', 'york',
    'card', 'jobs', 'provide', 'food', 'source', 'author', 'press', 'learn',
    'sale', 'around', 'print', 'course', 'canada', 'process', 'teen', 'room',
    'stock', 'credit', 'point', 'join', 'science', 'west', 'sales', 'look',
    'english', 'left', 'team', 'estate', 'select', 'windows', 'photos', 'thread',
    'week', 'note', 'live', 'large', 'gallery', 'table', 'however', 'june',
    'october', 'market', 'library', 'really', 'action', 'start', 'series', 'model',
    'plan', 'human', 'second', 'cost', 'movie', 'forums', 'march', 'better',
    'july', 'yahoo', 'going', 'medical', 'test', 'friend', 'come', 'server',
    'study', 'cart', 'staff', 'again', 'play', 'looking', 'issues', 'april',
    'never', 'users', 'street', 'topic', 'comment', 'things', 'working', 'against',
    'person', 'below', 'mobile', 'less', 'blog', 'party', 'payment', 'login',
    'student', 'offers', 'legal', 'above', 'recent', 'park', 'stores', 'side',
    'problem', 'give', 'memory', 'social', 'august', 'quote', 'story', 'sell',
    'options', 'rates', 'create', 'body', 'young', 'america', 'field', 'east',
    'paper', 'single', 'club', 'example', 'girls', 'latest', 'road', 'gift',
    'changes', 'night', 'hard', 'texas', 'four', 'poker', 'status', 'browse',
    'issue', 'range', 'seller', 'court', 'always', 'result', 'audio', 'light',
    'write', 'offer', 'blue', 'groups', 'easy', 'given', 'files', 'event',
    'release', 'request', 'china', 'making', 'picture', 'needs', 'might', 'month',
    'major', 'star', 'areas', 'future', 'space', 'hand', 'cards', 'london',
    'meeting', 'become', 'child', 'keep', 'enter', 'share', 'similar', 'garden',
    'schools', 'million', 'added', 'listed', 'baby', 'energy', 'popular', 'term',
    'film', 'stories', 'journal', 'reports', 'welcome', 'central', 'images', 'notice',
    'head', 'radio', 'until', 'cell', 'color', 'self', 'council', 'away',
    'track', 'archive', 'once', 'others', 'format', 'least', 'society', 'months',
    'safety', 'friends', 'sure', 'trade', 'edition', 'cars', 'tell', 'further',
    'updated', 'able', 'having', 'david', 'already', 'green', 'studies', 'close',
    'common', 'drive', 'several', 'gold', 'living', 'called', 'short', 'arts',
    'display', 'limited', 'powered', 'means', 'daily', 'beach', 'past', 'natural',
    'whether', 'five', 'upon', 'period', 'says', 'weather', 'land', 'average',
    'done', 'window', 'france', 'region', 'island', 'record', 'direct', 'records',
    'costs', 'style', 'front', 'update', 'parts', 'ever', 'early', 'miles',
    'sound', 'present', 'either', 'word', 'works', 'bill', 'written', 'talk',
    'federal', 'hosting', 'rules', 'final', 'adult', 'tickets', 'thing', 'centre',
    'cheap', 'kids', 'finance', 'true', 'minutes', 'else', 'mark', 'third',
    'rock', 'gifts', 'europe', 'reading', 'topics', 'tips', 'plus', 'auto',
    'cover', 'usually', 'edit', 'videos', 'percent', 'fast', 'fact', 'unit',
    'getting', 'global', 'tech', 'meet', 'player', 'lyrics', 'often', 'submit',
    'germany', 'amount', 'watch', 'feel', 'though', 'bank', 'risk', 'thanks',
    'deals', 'various', 'words', 'linux', 'james', 'weight', 'town', 'heart',
    'choose', 'points', 'error', 'camera', 'girl', 'toys', 'clear', 'golf',
    'receive', 'domain', 'methods', 'chapter', 'makes', 'loan', 'wide', 'beauty',
    'manager', 'india', 'taken', 'sort', 'models', 'michael', 'known', 'half',
    'cases', 'step', 'florida', 'simple', 'quick', 'none', 'license', 'paul',
    'friday', 'lake', 'whole', 'annual', 'later', 'basic', 'sony', 'shows',
    'google', 'church', 'method', 'active', 'figure', 'fire', 'holiday', 'chat',
    'enough', 'along', 'among', 'death', 'writing', 'speed', 'html', 'loss',
    'face', 'brand', 'higher', 'effects', 'created', 'yellow', 'kingdom', 'base',
    'near', 'thought', 'stuff', 'french', 'storage', 'japan', 'doing', 'loans',
    'shoes', 'entry', 'stay', 'nature', 'orders', 'africa', 'summary', 'turn',
    'mean', 'growth', 'notes', 'agency', 'king', 'monday', 'copy', 'drug',
    'pics', 'western', 'income', 'force', 'cash', 'overall', 'river', 'package',
    'seen', 'players', 'engine', 'port', 'album', 'stop', 'started', 'views',
    'plans', 'double', 'build', 'screen', 'types', 'soon', 'lines', 'across',
    'needed', 'season', 'apply', 'someone', 'held', 'printer', 'believe', 'effect',
    'asked', 'mind', 'sunday', 'casino', 'lost', 'tour', 'menu', 'volume',
    'cross', 'anyone', 'hope', 'silver', 'wish', 'inside', 'mature', 'role',
    'rather', 'weeks', 'came', 'supply', 'nothing', 'certain', 'running', 'lower',
    'union', 'jewelry', 'fine', 'names', 'robert', 'hour', 'skills', 'bush',
    'islands', 'advice', 'career', 'rental', 'leave', 'british', 'teens', 'huge',
    'woman', 'kind', 'sellers', 'middle', 'move', 'cable', 'taking', 'values',
    'coming', 'tuesday', 'object', 'lesbian', 'machine', 'logo', 'length', 'nice',
    'score', 'client', 'returns', 'capital', 'follow', 'sample', 'sent', 'shown',
    'england', 'culture', 'band', 'flash', 'lead', 'george', 'choice', 'went',
    'courses', 'airport', 'foreign', 'artist', 'outside', 'levels', 'channel', 'letter',
    'mode', 'phones', 'ideas', 'fund', 'summer', 'allow', 'degree', 'button',
    'homes', 'super', 'male', 'matter', 'custom', 'almost', 'took', 'located',
    'asian', 'editor', 'cause', 'song', 'cnet', 'focus', 'late', 'fall',
    'idea', 'rooms', 'female', 'thomas', 'primary', 'cancer', 'numbers', 'reason',
    'tool', 'browser', 'spring', 'answer', 'voice', 'purpose', 'feature', 'comes',
    'police', 'cameras', 'brown', 'hill', 'maps', 'deal', 'hold', 'ratings',
    'chicago', 'forms', 'glass', 'happy', 'smith', 'wanted', 'thank', 'safe',
    'unique', 'survey', 'prior', 'sport', 'ready', 'feed', 'animal', 'sources',
    'mexico', 'regular', 'secure', 'simply', 'station', 'round', 'paypal', 'option',
    'master', 'valley', 'rentals', 'built', 'blood', 'improve', 'hall', 'larger',
    'anti', 'earth', 'parents', 'nokia', 'impact', 'kitchen', 'strong', 'wedding',
    'ground', 'ship', 'owners', 'disease', 'paid', 'italy', 'perfect', 'hair',
    'classic', 'basis', 'command', 'cities', 'william', 'express', 'award', 'tree',
    'peter', 'ensure', 'thus', 'wall', 'extra', 'budget', 'rated', 'guides',
    'success', 'maximum', 'quite', 'amazon', 'warning', 'wine', 'horse', 'vote',
    'forward', 'flowers', 'stars', 'lists', 'owner', 'retail', 'animals', 'useful',
    'ways', 'rule', 'housing', 'takes', 'bring', 'catalog', 'trying', 'mother',
    'told', 'traffic', 'joined', 'input', 'feet', 'agent', 'valid', 'modern',
    'senior', 'ireland', 'door', 'grand', 'testing', 'trial', 'charge', 'units',
    'instead', 'cool', 'normal', 'wrote', 'ships', 'entire', 'leading', 'metal',
    'fitness', 'chinese', 'opinion', 'asia', 'uses', 'output', 'funds', 'greater',
    'likely', 'develop', 'artists', 'java', 'guest', 'seems', 'pass', 'trust',
    'session', 'multi', 'fees', 'century', 'skin', 'indian', 'prev', 'mary',
    'ring', 'grade', 'dating', 'pacific', 'filter', 'mailing', 'vehicle', 'longer',
    'behind', 'panel', 'floor', 'german', 'buying', 'match', 'default', 'require',
    'iraq', 'boys', 'outdoor', 'deep', 'morning', 'allows', 'rest', 'protein',
    'plant', 'pool', 'mini', 'partner', 'authors', 'boards', 'faculty', 'parties',
    'fish', 'mission', 'string', 'sense', 'pack', 'stage', 'goods', 'born',
    'unless', 'richard', 'race', 'target', 'except', 'ability', 'maybe', 'moving',
    'brands', 'places', 'pretty', 'spain', 'winter', 'battery', 'youth', 'boston',
    'debt', 'medium', 'core', 'break', 'sets', 'dance', 'wood', 'itself',
    'defined', 'papers', 'playing', 'awards', 'studio', 'reader', 'virtual', 'device',
    'answers', 'rent', 'remote', 'dark', 'apple', 'offered', 'theory', 'enjoy',
    'remove', 'surface', 'minimum', 'visual', 'host', 'variety', 'isbn', 'martin',
    'manual', 'block', 'agents', 'repair', 'fair', 'civil', 'steel', 'songs',
    'fixed', 'wrong', 'hands', 'finally', 'updates', 'desktop', 'classes', 'paris',
    'ohio', 'gets', 'sector', 'jersey', 'fully', 'father', 'quotes', 'officer',
    'driver', 'dead', 'respect', 'unknown', 'mike', 'trip', 'worth', 'poor',
    'teacher', 'eyes', 'workers', 'farm', 'georgia', 'peace', 'campus', 'showing',
    'coast', 'benefit', 'funding', 'devices', 'lord', 'grant', 'agree', 'fiction',
    'hear', 'watches', 'careers', 'beyond', 'goes', 'museum', 'blogs', 'wife',
    'former', 'hits', 'zone', 'complex', 'jack', 'flat', 'flow', 'parent',
    'spanish', 'setting', 'scale', 'stand', 'economy', 'highest', 'helpful', 'monthly',
    'frame', 'musical', 'angeles', 'path', 'chief', 'gives', 'bottom', 'detail',
    'laws', 'changed', 'heard', 'begin', 'royal', 'clean', 'switch', 'russian',
    'largest', 'african', 'titles', 'justice', 'connect', 'bible', 'basket', 'applied',
    'weekly', 'demand', 'suite', 'vegas', 'square', 'chris', 'advance', 'skip',
    'diet', 'army', 'auction', 'gear', 'allowed', 'correct', 'charles', 'nation',
    'selling', 'lots', 'piece', 'sheet', 'firm', 'seven', 'older', 'species',
    'jump', 'cells', 'module', 'resort', 'random', 'pricing', 'dvds', 'motion',
    'looks', 'fashion', 'monitor', 'trading', 'forest', 'calls', 'whose', 'couple',
    'giving', 'chance', 'vision', 'ball', 'ending', 'clients', 'actions', 'listen',
    'discuss', 'accept', 'naked', 'goal', 'sold', 'wind', 'markets', 'lowest',
    'highly', 'appear', 'lives', 'leather', 'palm', 'patient', 'actual', 'stone',
    'perhaps', 'persons', 'tests', 'village', 'amateur', 'pain', 'xbox', 'factors',
    'coffee', 'buyer', 'steve', 'easily', 'oral', 'ford', 'poster', 'edge',
    'root', 'closed', 'pink', 'zealand', 'balance', 'replies', 'shot', 'initial',
    'label', 'scott', 'canon', 'league', 'waste', 'minute', 'cold', 'chair',
    'fishing', 'effort', 'phase', 'fields', 'fantasy', 'letters', 'motor', 'context',
    'install', 'shirt', 'apparel', 'foot', 'mass', 'crime', 'count', 'breast',
    'johnson', 'quickly', 'dollars', 'claim', 'driving', 'surgery', 'patch', 'heat',
    'wild', 'kansas', 'miss', 'doctor', 'task', 'reduce', 'brought', 'himself',
    'enable', 'santa', 'leader', 'diamond', 'israel', 'soft', 'servers', 'alone',
    'seconds', 'jones', 'arizona', 'keyword', 'flight', 'fuel', 'walk', 'italian',
    'wait', 'pocket', 'saint', 'rose', 'freedom', 'drugs', 'joint', 'premium',
    'fresh', 'upgrade', 'factor', 'growing', 'stream', 'pick', 'hearing', 'eastern',
    'therapy', 'entries', 'dates', 'signed', 'upper', 'serious', 'prime', 'samsung',
    'limit', 'began', 'louis', 'steps', 'errors', 'shops', 'efforts', 'creek',
    'worked', 'urban', 'sorted', 'myself', 'tours', 'load', 'labor', 'admin',
    'nursing', 'defense', 'tags', 'heavy', 'covered', 'guys', 'expert', 'protect',
    'drop', 'solid', 'became', 'orange', 'prevent', 'theme', 'rich', 'marine',
    'guitar', 'finding', 'ipod', 'saying', 'spirit', 'claims', 'seem', 'affairs',
    'touch', 'towards', 'goals', 'hire', 'suggest', 'branch', 'charges', 'serve',
    'reasons', 'magic', 'mount', 'smart', 'talking', 'gave', 'ones', 'latin',
    'avoid', 'manage', 'corner', 'rank', 'oregon', 'element', 'birth', 'virus',
    'abuse', 'quarter', 'tables', 'define', 'racing', 'facts', 'kong', 'column',
    'plants', 'faith', 'chain', 'avenue', 'missing', 'died', 'sitemap', 'moved',
    'houston', 'reach', 'mental', 'viewed', 'moment', 'inch', 'attack', 'sorry',
    'centers', 'opening', 'damage', 'reserve', 'recipes', 'gamma', 'plastic', 'produce',
    'snow', 'placed', 'truth', 'counter', 'failure', 'follows', 'weekend', 'dollar',
    'camp', 'ontario', 'films', 'bridge', 'native', 'fill', 'owned', 'draft',
    'chart', 'played', 'jesus', 'readers', 'clubs', 'jackson', 'equal', 'shirts',
    'profit', 'leaders', 'posters', 'expect', 'parking', 'russia', 'gone', 'codes',
    'kinds', 'seattle', 'golden', 'teams', 'fort', 'senate', 'forces', 'funny',
    'brother', 'gene', 'turned', 'tried', 'disc', 'pattern', 'boat', 'named',
    'theatre', 'laser', 'earlier', 'sponsor', 'icon', 'indiana', 'harry', 'objects',
    'ends', 'delete', 'evening', 'nuclear', 'taxes', 'mouse', 'signal', 'issued',
    'brain', 'sexual', 'dream', 'false', 'cast', 'flower', 'felt', 'passed',
    'falls', 'soul', 'aids', 'promote', 'stated', 'stats', 'hawaii', 'appears',
    'carry', 'flag', 'decided', 'covers', 'hello', 'designs', 'tourism', 'adults',
    'clips', 'savings', 'graphic', 'atom', 'binding', 'brief', 'ended', 'winning',
    'eight', 'iron', 'script', 'served', 'wants', 'void', 'dining', 'alert',
    'atlanta', 'dakota', 'disk', 'queen', 'credits', 'clearly', 'handle', 'sweet',
    'desk', 'pubmed', 'dave', 'diego', 'hong', 'vice', 'truck', 'enlarge',
    'revenue', 'measure', 'votes', 'duty', 'looked', 'bear', 'gain', 'ocean',
    'flights', 'experts', 'signs', 'lack', 'depth', 'iowa', 'logged', 'laptop',
    'vintage', 'train', 'exactly', 'explore', 'concept', 'nearly', 'reality', 'forgot',
    'origin', 'knew', 'gaming', 'feeds', 'billion', 'faster', 'dallas', 'bought',
    'nations', 'route', 'broken', 'frank', 'alaska', 'zoom', 'blow', 'battle',
    'anime', 'speak', 'query', 'clip', 'equity', 'speech', 'wire', 'rural',
    'shared', 'sounds', 'tape', 'judge', 'spam', 'acid', 'bytes', 'cent',
    'forced', 'fight', 'height', 'null', 'zero', 'speaker', 'filed', 'obtain',
    'offices', 'remain', 'managed', 'failed', 'roll', 'korea', 'banks', 'secret',
    'bath', 'kelly', 'leads', 'austin', 'toronto', 'theater', 'springs', 'andrew',
    'perform', 'healthy', 'font', 'assets', 'injury', 'joseph', 'drivers', 'lawyer',
    'figures', 'married', 'sharing', 'portal', 'waiting', 'beta', 'fail', 'gratis',
    'banking', 'brian', 'toward', 'assist', 'conduct', 'calling', 'jazz', 'serving',
    'bags', 'miami', 'comics', 'matters', 'houses', 'postal', 'wear', 'wales',
    'minor', 'finish', 'noted', 'reduced', 'physics', 'rare', 'spent', 'extreme',
    'samples', 'davis', 'daniel', 'bars', 'removed', 'helps', 'singles', 'cycle',
    'amounts', 'contain', 'dual', 'rise', 'sleep', 'bird', 'brazil', 'static',
    'scene', 'hunter', 'lady', 'crystal', 'famous', 'writer', 'fans', 'drink',
    'academy', 'dynamic', 'gender', 'dell', 'seat', 'colour', 'vendor', 'intel',
    'bids', 'regions', 'junior', 'toll', 'cape', 'rings', 'meaning', 'mine',
    'ladies', 'henry', 'ticket', 'guess', 'agreed', 'whom', 'soccer', 'math',
    'import', 'posting', 'instant', 'viewing', 'christ', 'dogs', 'aspects', 'austria',
    'ahead', 'moon', 'scheme', 'utility', 'preview', 'manner', 'matrix', 'devel',
    'despite', 'turkey', 'proper', 'degrees', 'delta', 'fear', 'seeking', 'inches',
    'phoenix', 'shares', 'comfort', 'colors', 'wars', 'cisco', 'kept', 'alpha',
    'appeal', 'cruise', 'bonus', 'beat', 'disney', 'adobe', 'smoking', 'becomes',
    'drives', 'arms', 'alabama', 'trees', 'achieve', 'dress', 'dealer', 'utah',
    'nearby', 'carried', 'happen', 'hide', 'refer', 'miller', 'clothes', 'caused',
    'luxury', 'babes', 'frames', 'indeed', 'circuit', 'layer', 'printed', 'slow',
    'removal', 'easier', 'faqs', 'nine', 'adding', 'mostly', 'eric', 'spot',
    'taylor', 'prints', 'spend', 'factory', 'revised', 'grow', 'optical', 'amazing',
    'clock', 'suites', 'feeling', 'hidden', 'serial', 'relief', 'ratio', 'rain',
    'onto', 'planet', 'copies', 'recipe', 'permit', 'seeing', 'proof', 'diff',
    'tennis', 'bass', 'bedroom', 'empty', 'hole', 'pets', 'ride', 'orlando',
    'bureau', 'maine', 'pair', 'ideal', 'specs', 'pieces', 'parks', 'dinner',
    'lawyers', 'sydney', 'stress', 'cream', 'runs', 'trends', 'yeah', 'boxes',
    'hills', 'fourth', 'advisor', 'evil', 'aware', 'wilson', 'shape', 'irish',
    'remains', 'firms', 'euro', 'generic', 'usage', 'charts', 'mixed', 'census',
    'peak', 'exist', 'wheel', 'transit', 'salt', 'compact', 'poetry', 'lights',
    'angel', 'bell', 'keeping', 'attempt', 'matches', 'width', 'noise', 'engines',
    'forget', 'array', 'stephen', 'climate', 'alcohol', 'greek', 'sister', 'walking',
    'explain', 'smaller', 'newest', 'jeff', 'extent', 'sharp', 'lane', 'kill',
    'export', 'modules', 'sweden', 'occur', 'knows', 'concern', 'backup', 'holding',
    'trouble', 'spread', 'coach', 'kevin', 'expand', 'jordan', 'ages', 'plug',
    'cook', 'affect', 'virgin', 'raised', 'dealers', 'helping', 'perl', 'bike',
    'totally', 'plate', 'blonde', 'lose', 'organic', 'seek', 'albums', 'cheats',
    'guests', 'hosted', 'tony', 'nevada', 'kits', 'agenda', 'anyway', 'tracks',
    'logic', 'prince', 'circle', 'soil', 'grants', 'edward', 'leaving', 'matt',
    'cooking', 'respond', 'sizes', 'plain', 'exit', 'entered', 'iran', 'keys',
    'launch', 'wave', 'costa', 'belgium', 'holy', 'acts', 'mesh', 'trail',
    'symbol', 'crafts', 'highway', 'buddy', 'dean', 'setup', 'poll', 'booking',
    'fiscal', 'styles', 'denver', 'unix', 'filled', 'bond', 'notify', 'blues',
    'portion', 'scope', 'cables', 'cotton', 'biology', 'dental', 'killed', 'border',
    'ancient', 'debate', 'starts', 'causes', 'leisure', 'learned', 'opened', 'husband',
    'crazy', 'britain', 'concert', 'scores', 'comedy', 'adopted', 'weblog', 'linear',
    'bears', 'jean', 'carrier', 'edited', 'visa', 'mouth', 'jewish', 'meter',
    'linked', 'reflect', 'pure', 'deliver', 'wonder', 'lessons', 'fruit', 'begins',
    'reform', 'lens', 'alerts', 'treated', 'draw', 'mysql', 'assume', 'confirm',
    'warm', 'neither', 'lewis', 'howard', 'offline', 'leaves', 'replace', 'babe',
    'checks', 'reached', 'safari', 'sugar', 'crew', 'legs', 'stick', 'allen',
    'enabled', 'genre', 'slide', 'montana', 'tested', 'rear', 'enhance', 'exact',
    'bound', 'adapter', 'node', 'formal', 'lock', 'hockey', 'storm', 'micro',
    'laptops', 'mile', 'showed', 'editors', 'mens', 'threads', 'bowl', 'supreme',
    'tank', 'dolls', 'navy', 'cancel', 'limits', 'weapons', 'paint', 'delay',
]

def generate_passphrase(num_words=4, separator="-", add_number=True):
    """
    Generate a Diceware-style passphrase using secrets.choice
    (cryptographically secure), not the random module.

    Suggested when a checked password comes back weak, as an
    alternative that's easier to remember than a random string
    of symbols but still has real entropy behind it.
    """

    chosen_words = [
        secrets.choice(WORDLIST)
        for _ in range(num_words)
    ]

    # Capitalize each word for readability
    chosen_words = [word.capitalize() for word in chosen_words]

    passphrase = separator.join(chosen_words)

    if add_number:
        # Append a random 2-digit number for a little extra entropy
        passphrase += separator + str(secrets.randbelow(90) + 10)

    return passphrase


def calculate_passphrase_entropy(num_words, add_number=True):
    """
    Entropy in bits for a passphrase generated the same way as
    generate_passphrase(), so the UI can show *why* it's strong,
    not just hand over a string.
    """

    bits_per_word = math.log2(len(WORDLIST))

    total_bits = bits_per_word * num_words

    if add_number:
        # 90 possible two-digit numbers (10-99)
        total_bits += math.log2(90)

    return round(total_bits, 1)


def suggest_passphrases(count=3, num_words=5):
    """
    Return a small set of passphrase suggestions along with
    their entropy, for the results page to display when a
    checked password is weak.

    5 words (+ the trailing number) lands around 60+ bits of
    entropy, which crosses into the "Strong" band on our own
    entropy scoring in entropy_checker.py -- so a suggestion
    PassShield offers should itself pass PassShield's checks.
    """

    suggestions = []

    for _ in range(count):

        passphrase = generate_passphrase(num_words=num_words)

        suggestions.append({
            "passphrase": passphrase,
            "entropy_bits": calculate_passphrase_entropy(num_words),
            # Plain-language strength label for the results page --
            # the bits number stays available for anyone who wants
            # the technical detail, but isn't shown by default
            "strength_label": "Strong & easy to remember"
        })

    return suggestions


# Run only when this file is executed directly
if __name__ == "__main__":

    print("\n--- PassShield Passphrase Suggestions ---\n")

    for suggestion in suggest_passphrases():

        print(suggestion["passphrase"], "  (", suggestion["entropy_bits"], "bits )")