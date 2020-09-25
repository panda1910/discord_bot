table_data = [[3,'callmepandey',2],
              [4,'Saitama',2],
              [5,'!👑!Fire Feathers!👑!',2]]

mess = "Top 10 members:\n"
mess += "{: <5} {: <8} {: <10}\n".format("Rank", "User", "Level")
for row in table_data:
    mess += "{: <5} {: <8} {: <10}\n".format(row[0],row[2],row[1])
print(mess)
# import subprocess
# import psutil
# import time
#
# done = False
# def kill(proc_pid):
#     process = psutil.Process(proc_pid)
#     for proc in process.children(recursive=True):
#         proc.kill()
#     process.kill()
#
# def code():
#     print("Running t1")
#     #os.system('python cogs/p_util/t1.py < cogs/p_util/pin.txt > cogs/p_util/pout.txt')
#     proc = subprocess.Popen(['python', 'cogs/p_util/t1.py', '<cogs/p_util/pin.txt', '>cogs/p_util/pout.txt'],
#                             shell=True)
#     try:
#         time.sleep(1)
#         poll = proc.poll()
#         if poll == None:
#             proc.wait(timeout=3)
#             print("Second dip worked")
#         else:
#             print("I was a success")
#
#     except subprocess.TimeoutExpired:
#         print("Killed")
#         kill(proc.pid)
#
# code()
#
#
#
#
# #     # time.sleep(1)
# #     # poll = proc.poll()
# #     # if poll == None:
# #     #     print("pid: ", proc.pid)
# #     #     pid = proc.pid
# #     #     os.kill(pid, signal.SIGTERM)
# #     #     print("Sent the command lets see")
# #     # else:
# #     #     done = True
# #
# #     '''file = open("cogs/p_util/pout.txt", "w")
# #     file.close()
# #     file = open("cogs/p_util/plog.txt", "w")
# #     file.close()
# #     file = open("cogs/p_util/pin.txt", "w")
# #     file.close()'''
# #     '''while True:
# #         time.sleep(0.5)
# #         print("Inf")'''
# #
# #
# # def check(num):
# #     global done
# #     if done==False:
# #         print("Done is False")
# #         time.sleep(2)
# #         global killit
# #         if not done:
# #             killit = True
# #         else:
# #             print("Success on second dip")
# #     else:
# #         print("Success")
# #
# #
# # t1 = threading.Thread(target=code, args=(10,))
# # t2 = threading.Thread(target=check, args=(10,))
# # t1.daemon = True
# # t1.start()
# #
# #
# # t2.start()
# # t2.join()
# # if killit:
# #     print("Yes kill")
# #
# #     sys.exit()
# # t1.join()
# # print("Done!")
# # #proc = subprocess.Popen(['python', 'cogs/p_util/t1.py', '<cogs/p_util/pin.txt','>cogs/p_util/pout.txt'],shell=True)
# #
