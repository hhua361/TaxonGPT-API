__author__ = 'huang'

'''
GeneGPT: teach LLMs to use NCBI API
'''

import json
#导入OpenAI的Python库。这个库提供了与OpenAI API进行交互的功能
import openai
#导入一个名为config的模块，这通常是一个自定义模块，包含配置信息，比如API密钥等。
import config
#输入openai在本地的API来实现
openai.api_key = config.API_KEY

import os
import re
import sys
import time
#从urllib库中导入request模块，它用于打开和读取URLs（统一资源定位符），是Python用于网络请求的一个接口。
import urllib.request
#定义了一个关于call_api的函数，旨在通过给定的URL调用一个API，并返回API的响应。
def call_api(url):
	#在执行任何网络请求前，先让程序暂停一秒，用于避免因请求过快而违反API的速率限制or减少对服务器的负担
	time.sleep(1)
	#将URL中所有的空格字符替换成+号。因为在URL中，加号是空格的一种编码方式。用于对URL进行清理的一种常见做法，用于确保URL的格式正确，特别是在将查询参数附加到URL时
	url = url.replace(' ', '+')
	#将处理后的URL打印到控制台。这对于调试目的是有帮助的，可以让开发者看到正在调用的确切URL。
	print(url)

	#使用urllib.request.Request类创建一个表示HTTP请求的对象。这个请求对象req包含了要访问的URL以及可以包含的其他HTTP头信息。
	req = urllib.request.Request(url)
	#这行代码打开上一步创建的请求req，并返回一个响应对象response。使用with语句确保在完成请求后正确关闭连接。
	with urllib.request.urlopen(req) as response:
		#从响应对象中读取内容。response.read()方法会读取服务器返回的所有数据，并将其作为字节串存储在变量call中。
		call = response.read()

	return call
#‘call_api’函数通过给定的URL进行API调用，处理URL格式，执行HTTP请求

#通过定义一个函数来实现提供提示，来帮助将web api导入来构建一个提示信息
def get_prompt_header(mask):
	'''
	mask: [1/0 x 6], denotes whether each prompt component is used

	output: prompt
	'''
	#函数构造了一系列URL，每个URL对应于一个特定的NCBI API 的请求，这些请求分别对应用于从NCBI的不同数据库检索信息，以及执行基因序列的BLAST搜索
	url_1 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&retmax=5&retmode=json&sort=relevance&term=LMP10'
	call_1 = call_api(url_1)

	url_2 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&retmax=5&retmode=json&id=19171,5699,8138'
	call_2 = call_api(url_2)

	url_3 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=snp&retmax=10&retmode=json&id=1217074595' 
	call_3 = call_api(url_3)

	url_4 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=omim&retmax=20&retmode=json&sort=relevance&term=Meesmann+corneal+dystrophy'
	call_4 = call_api(url_4)

	url_5 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=omim&retmax=20&retmode=json&id=618767,601687,300778,148043,122100'
	call_5 = call_api(url_5)
	#其中URL6 用于进行提交一个BLAST任务，用于在nt库数据库中搜索指定的基因序列
	url_6 = 'https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Put&PROGRAM=blastn&MEGABLAST=on&DATABASE=nt&FORMAT_TYPE=XML&QUERY=ATTCTGCCTTTAGTAATTTGATGACAGAGACTTCTTGGGAACCACAGCCAGGGAGCCACCCTTTACTCCACCAACAGGTGGCTTATATCCAATCTGAGAAAGAAAGAAAAAAAAAAAAGTATTTCTCT&HITLIST_SIZE=5'
	call_6 = call_api(url_6)
	#考虑到URL6与其他几个步骤之间是异步执行的，因此在call_6中提取一个任务ID（RID）来构建URL7
	rid = re.search('RID = (.*)\n', call_6.decode('utf-8')).group(1)
	#该步骤用于处理NCBI的BLAST查询的过程中，用于检索异步执行的BLAST任务的结果
	#异步执行：由于BLAST搜索可能需要一段时间来处理，尤其是当搜索的数据库很大或查询序列很长时，BLAST任务是异步执行的。这意味着当你提交一个BLAST搜索请求时，任务开始执行，但你需要稍后再来检查结果。
	#任务ID（RID）提取：当你提交BLAST查询后，系统会为这个任务分配一个唯一的任务ID（RID），你可以使用这个ID来查询任务的执行状态和结果。在call_6的响应中提取RID，是为了随后能用它检索BLAST任务的结果。
	#等待结果：由于BLAST任务是异步执行的，因此在尝试检索结果之前需要等待一段时间，以确保任务有足够的时间完成。在这个例子中，代码中通过time.sleep(30)实现了等待30秒，这是一个简单的方式来给BLAST任务处理提供足够的时间。
	#异步执行允许程序在等待一个长时间运行的任务完成时继续执行其他任务，从而提高了程序的效率和响应性。
	#由于BLAST的过程需要一个长时间的并需要其他任务。
	url_7 = f'https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&FORMAT_TYPE=Text&RID={rid}'
	time.sleep(30)
	call_7 = call_api(url_7)

	prompt = ''
	prompt += 'Hello. Your task is to use NCBI Web APIs to answer genomic questions.\n'
	#+=用于字符串连接操作，即将右侧的字符串添加（或连接）到左侧字符串的末尾，这意味着在整个回答的末端会出现这句话
	#prompt += 'There are two types of Web APIs you can use: Eutils and BLAST.\n\n'
	#所以这一部分的mask指令都是关于通过指定数字（0-6）之间来指定进行什么功能

	if mask[0]:
		# Doc 0 is about Eutils
		#介绍了如何构造Eutils的API调用URL，包括esearch、efetch和esummary三种操作，以及如何指定数据库（gene、snp、omim）和查询参数（retmax、term或id）。
		prompt += 'You can call Eutils by: "[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/{esearch|efetch|esummary}.fcgi?db={gene|snp|omim}&retmax={}&{term|id}={term|id}]".\n'
		prompt += 'esearch: input is a search term and output is database id(s).\n'
		prompt += 'efectch/esummary: input is database id(s) and output is full records or summaries that contain name, chromosome location, and other information.\n'
		prompt += 'Normally, you need to first call esearch to get the database id(s) of the search term, and then call efectch/esummary to get the information with the database id(s).\n'
		prompt += 'Database: gene is for genes, snp is for SNPs, and omim is for genetic diseases.\n\n'

	if mask[1]:
		# Doc 1 is about BLAST
		#这个则是调用这个使用BLAST的api指令，通过使用mask1来调用BLAST数据库的web api
		prompt += 'For DNA sequences, you can use BLAST by: "[https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD={Put|Get}&PROGRAM=blastn&MEGABLAST=on&DATABASE=nt&FORMAT_TYPE={XML|Text}&QUERY={sequence}&HITLIST_SIZE={max_hit_size}]".\n'
		prompt += 'BLAST maps a specific DNA {sequence} to its chromosome location among different specices.\n'
		prompt += 'You need to first PUT the BLAST request and then GET the results using the RID returned by PUT.\n\n'
#mask[2]至mask[5]的使用是为了控制是否在提示信息中包含特定的示例问题和答案。，其中包含通过提供这些特定的例子来进行prompt，类似于一种ICS，来帮助LLM进行NCBI
	if any(mask[2:]):
		prompt += 'Here are some examples:\n\n'

	if mask[2]:
		# Example 1 is from gene alias task 
		prompt += f'Question: What is the official gene symbol of LMP10?\n'
		prompt += f'[{url_1}]->[{call_1}]\n' 
		prompt += f'[{url_2}]->[{call_2}]\n'
		prompt += f'Answer: PSMB10\n\n'

	if mask[3]:
		# Example 2 is from SNP gene task
		prompt += f'Question: Which gene is SNP rs1217074595 associated with?\n'
		prompt += f'[{url_3}]->[{call_3}]\n'
		prompt += f'Answer: LINC01270\n\n'

	if mask[4]:
		# Example 3 is from gene disease association
		prompt += f'Question: What are genes related to Meesmann corneal dystrophy?\n'
		prompt += f'[{url_4}]->[{call_4}]\n'
		prompt += f'[{url_5}]->[{call_5}]\n'
		prompt += f'Answer: KRT12, KRT3\n\n'

	if mask[5]:
		# Example 4 is for BLAST
		prompt += f'Question: Align the DNA sequence to the human genome:ATTCTGCCTTTAGTAATTTGATGACAGAGACTTCTTGGGAACCACAGCCAGGGAGCCACCCTTTACTCCACCAACAGGTGGCTTATATCCAATCTGAGAAAGAAAGAAAAAAAAAAAAGTATTTCTCT\n'
		prompt += f'[{url_6}]->[{rid}]\n'
		prompt += f'[{url_7}]->[{call_7}]\n'
		prompt += f'Answer: chr15:91950805-91950932\n\n'

	return prompt


if __name__ == '__main__':
	# rough number of chars for truncating 
	# codex accepts 8k tokens ~ 18k chars 
	cut_length = 18000

	# str_mask is a string of six 0/1 marking whether a in-context learning component is used 
	# six digits correspond to Dc. 1-2, Dm. 1-4
	#获取命令行的第一个参数，sys.argv[1]是传递给脚本的第一个参数。在这个上下文中，预期这个参数是一个字符串，由六个数字组成，每个数字都是0或1，代表不同的功能或示例是否应该被包含在生成的提示信息中。
	#这将关于mask的prompt
	str_mask = sys.argv[1]
	#mask列表中的每个元素都代表了是否启用相应的功能或示例。通过使用将mask转化成布尔值（转化成整数），来决定这些mask的调用
	mask = [bool(int(x)) for x in str_mask]
	#将构造好的mask列表作为参数传递。这个函数根据mask中的值动态生成提示信息，并将这个提示信息赋值给变量prompt。函数的具体实现根据mask的不同值选择性地包括不同的说明和示例问题，以此来定制提示信息的内容。
	prompt = get_prompt_header(mask)

	# results are saved in the dir of six digits
	#这段代码用于在文件系统中创建一个目录，目录名由命令行参数str_mask指定，通常是一个由六个数字组成的字符串。这个目录用于存放脚本运行的结果。
	if not os.path.isdir(str_mask):
		os.mkdir(str_mask)
	#时间戳初始化 (prev_call) 通常用于后续操作中计算时间差，例如，评估某些操作的执行时间，或者在需要按一定时间间隔进行操作时确保间隔被正确维持。通过使用时间来确定是否在进行正常的对待
	# initialize 
	prev_call = time.time()
	#加载JSON文件 (qas) 提供了一种方便的方式来加载和处理静态数据，特别是当这些数据以结构化的格式存储在文件中时。
	qas = json.load(open('data/geneturing.json'))
	#遍历一个字典（qas），检查每个任务是否已经完成，并根据条件决定是否跳过当前循环迭代。通过遍历这些任务
	for task, info in qas.items():
		#这行代码检查以str_mask命名的目录中是否存在名为{task}.json的文件。如果这个文件存在，说明相应的任务可能已经被执行并完成了。
		if os.path.exists(os.path.join(str_mask, f'{task}.json')):
			# 如果任务结果文件存在，这行代码加载该结果文件
			preds = json.load(open(os.path.join(str_mask, f'{task}.json')))
			#这行代码检查preds列表的长度是否为50。如果是，说明任务已经完成（基于某种规则假设任务完成时会有50个结果条目），然后使用continue语句跳过当前循环的剩余部分，直接开始下一个任务的处理。这样做可以避免重复处理已经完成的任务。
			if len(preds) == 50: continue
		# 初始化一个名为output的空列表，用于存储任务处理的结果或输出。
		output = []
		#打印当前正在处理的任务名称或标识符，{task}是之前从字典qas中遍历得到的任务键值。
		print(f'Doing task {task}')
		#遍历当前任务info中的每一个问题及其答案。info是与当前task相关联的值，它包含了问题和答案的键值对。
		for question, answer in info.items():
			#在处理每个新问题之前，打印一个分隔提示，表明一个新的问题实例开始。
			print('---New Instance---')
			#打印当前问题的文本。
			print(question)
			#将之前构建的提示信息prompt（可能包含关于如何使用API的指导）与当前问题的文本合并，创建一个包含问题文本的新提示信息q_prompt。
			q_prompt = prompt + f'Question: {question}\n'

			# 初始化一个空列表prompts，用于保存与当前问题相关的所有提示信息或日志。
			prompts = []

			# 初始化一个计数器num_calls，用于记录处理当前问题时进行的API调用次数。记录NCBI API的调用次数
			num_calls = 0

			#这段代码执行一个循环，用于调用一个模型（如OpenAI的GPT）来处理一个问题，并控制请求的发送频率。通过控制请求的发送频率来控制整体运行的时间和进度，避免进一步
			#这创建了一个无限循环，通常需要在循环内部某处明确地跳出循环（例如，通过break语句）以避免无限执行。
			while True:
				#检查构建的问题提示信息q_prompt的长度是否超过了某个阈值cut_length。确定了使用序列的相关强度
				if len(q_prompt) > cut_length:
					# truncate from the start
					# 将q_prompt从开始处截断，只保留其末尾的cut_length个字符。这是为了满足某些API调用对输入长度有限制的情况，确保请求不会因为提示信息过长而失败。
					q_prompt = q_prompt[len(q_prompt) - cut_length:]

				#该指令调用了需要用到的openAi模型调用的相关参数
				body = {
				  "model": "code-davinci-002",
				  "prompt": q_prompt,
				  "max_tokens": 512,
				  "temperature": 0,
				  "stop": ['->', '\n\nQuestion'],
				  "n": 1
				}
				#计算自上一次API调用以来经过的时间
				delta = time.time() - prev_call
				
				# codex has a rate limite of 20 requests / min
				# it's a workaround
				# 这段代码是为了管理和遵守OpenAI Codex模型的请求频率限制，确保不会因为请求过于频繁而违反API的使用政策或触发限流措施
				# 3.1秒是根据20次/分钟的限制计算得出的大约间隔时间（60秒/20次 ≈ 3秒），这里使用3.1秒是为了提供一点额外的缓冲，以确保不会意外超过限制。
				if delta < 3.1:
					time.sleep(3.1 - delta)
				#这段代码执行一个尝试-异常处理（try-except）块，用于调用OpenAI的API并处理可能发生的特定错误。
				try:
					# 首先更新prev_call变量为当前时间，这是为了记录API调用的起始时间，以便控制请求的频率。
					prev_call = time.time()
					# 这行代码使用OpenAI Python客户端库发起一个API请求。openai.Completion.create()方法是用于生成文本的API调用，body变量包含了请求所需的所有参数（如模型名、输入提示、最大生成令牌数等）。
					response = openai.Completion.create(**body)
				# 如果在API请求过程中发生InvalidRequestError异常（这通常是由于请求的格式不正确或违反了API的使用规则），则执行except块中的代码。这种错误可能是因为请求体body的内容不符合API的要求，比如输入过长等。
				except openai.error.InvalidRequestError:
					# 将一个包含问题、答案、错误类型（这里是'lengthError'）和已经收集的提示信息的列表添加到output列表中。这样做旨在记录发生错误的问题及其上下文，方便后续的分析和调试。
					output.append([question, answer, 'lengthError', prompts])
					# 由于遇到了错误，break语句会立即退出当前的循环。这意味着如果在处理某个任务的某个问题时遇到InvalidRequestError，程序将不会继续尝试处理该任务的其他问题，而是跳出循环，可能会继续处理下一个任务（取决于这段代码在循环结构中的位置）。
					break
				#处理了从openAI接收到的响应
				# 这行代码从API的响应中提取文本内容。response是API返回的数据，通过text提取在这个选项中实际获得的文本
				text = response['choices'][0]['text']
				print(text)
				# 这行代码将变量num_calls的值增加1，num_calls用于记录在处理当前问题时已经进行的API调用次数。这对于控制API调用频率或评估调用成本很有用。
				num_calls += 1
				# 这相当于储存了一个关于API的历史记录，这行代码将当前的问题提示q_prompt和API返回的文本text作为一个列表添加到prompts列表中。这样做可以保存每个问题及其相应的AI生成文本，方便后续的分析或记录。
				prompts.append([q_prompt, text])
				# 提取生成文本中的特定信息（如URL）
				url_regex = r'\[(https?://[^\[\]]+)\]'
				matches = re.findall(url_regex, text)
				# 如果在上一步中通过正则表达式匹配到了URL，
				if matches:
					# 取出匹配到的第一个URL用于后续操作。
					url = matches[0]
					
					# 如果URL包含blast并且是一个Get请求，代码将暂停30秒。这是因为BLAST查询通常需要时间在NCBI服务器上执行，等待是为了确保BLAST查询完成并且结果可以被检索。
					if 'blast' in url and 'Get' in url: time.sleep(30)
					# 使用之前定义的call_api函数对找到的URL进行API调用，并将响应赋值给call。
					call = call_api(url)
					#如果URL是一个BLAST的Put请求（即提交BLAST查询），通过正则表达式从响应中提取请求ID（RID），并将其用于之后的Get请求以检索BLAST结果
					if 'blast' in url and 'Put' in url:
						rid = re.search('RID = (.*)\n', call.decode('utf-8')).group(1)
						call = rid
					# 如果call（即API调用的响应或BLAST查询的RID）的长度超过10000字符，将其截断至前10000字符。这可能是为了避免处理过大的数据量，或满足特定的数据处理需求。
					if len(call) > 10000:
						call = call[:10000]
					# 将API调用的结果或处理后的信息追加到问题提示q_prompt中，以便于下一步的操作或记录。
					q_prompt = f'{q_prompt}{text}->[{call}]\n'

				# 如果没有找到任何URL（即matches为空），则将当前问题、答案、文本响应和已收集的提示信息作为一个列表添加到output列表中，并终止当前循环。
				else:
					output.append([question, answer, text, prompts])
					break

				# 果API调用次数num_calls达到或超过10次，认为可能进入了死循环，因此将当前问题、答案和一个错误标记（'numError'）添加到output列表中，并终止循环。
				if num_calls >= 10:
					output.append([question, answer, 'numError', prompts])
					break

		# 果API调用次数num_calls达到或超过10次，认为可能进入了死循环，因此将当前问题、答案和一个错误标记（'numError'）添加到output列表中，并终止循环。
		with open(os.path.join(str_mask, f'{task}.json'), 'w') as f:
			json.dump(output, f, indent=4)
