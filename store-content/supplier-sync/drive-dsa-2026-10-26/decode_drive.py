import json,base64,glob,os,sys
out='drive-img'; os.makedirs(out,exist_ok=True)
done=json.load(open('drive-done.json')) if os.path.exists('drive-done.json') else {}
for f in glob.glob('/root/.claude/projects/-home-user-Excellent-Tiling-Services-/e875297c-2cd6-5856-97ee-9fb5b6b7c7ba/tool-results/mcp-Google_Drive-download_file_content-*.txt'):
    try: d=json.load(open(f))
    except Exception as e: print('skip',f,e); continue
    if d['id'] in done: continue
    p=os.path.join(out,d['id']+'_'+d['title'].replace('/','_'))
    open(p,'wb').write(base64.b64decode(d['content'])); done[d['id']]=p; print('ok',d['title'],os.path.getsize(p)); os.remove(f)
json.dump(done,open('drive-done.json','w'),indent=1)
print(len(done),'files')
