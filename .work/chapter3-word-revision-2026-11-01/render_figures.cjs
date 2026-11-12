const fs=require('fs');
const path=require('path');
const {chromium}=require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const sharp=require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const graphs={
 a:`flowchart TD
 S([Open installed game]) --> L[Read available local progress]
 D[(Device storage)] -.->|Load| L
 L --> M[Main Menu]
 M -->|Settings| Settings[Settings]
 M -->|Tutorial| T[Tutorial]
 M -->|Exit| E([Exit])
 M -->|Play| Map[B: Landform Map]
 Map --> Ep[Choose an unlocked episode]
 Ep --> Level[Choose an available mode and level]
 Level --> A([A: Lesson and gameplay])`,
 b:`flowchart TD
 A([A: Start selected level]) --> Lesson[Short lesson]
 Lesson --> Explore[Explore and collect]
 Explore --> Info[Item illustration,<br/>name and description]
 Info --> Explore
 Explore -->|Level completed| Results[Collected items,<br/>review and stars]
 Results -.->|Progress data| Store[(Device storage)]
 Results -->|Replay| Lesson
 Results -->|Continue| Check{Episode<br/>requirements met?}
 Check -->|No| Next[Next available level]
 Next --> Lesson
 Check -->|Yes| Summary[Episode summary]
 Summary --> All{All four episodes<br/>completed?}
 All -->|No| Unlock[Unlock next episode]
 Unlock --> B([B: Landform Map])
 All -->|Yes| Final([Final completion])`
};
(async()=>{let browser;try{
 browser=await chromium.launch({headless:true,channel:'msedge'});
 const page=await browser.newPage();
 await page.setContent('<!doctype html><html><body></body></html>');
 await page.addScriptTag({url:'https://cdn.jsdelivr.net/npm/mermaid@10.9.3/dist/mermaid.min.js'});
 const reports=[];
 for(const [id,graph] of Object.entries(graphs)){
  fs.writeFileSync(path.join(__dirname,`flow-${id}.mmd`),graph);
  const svg=await page.evaluate(async({id,graph})=>{
   mermaid.initialize({startOnLoad:false,securityLevel:'strict',theme:'base',themeVariables:{fontFamily:'Arial',fontSize:'22px',primaryColor:'#ffffff',primaryTextColor:'#000000',primaryBorderColor:'#303030',lineColor:'#303030',edgeLabelBackground:'#ffffff',background:'#ffffff'},flowchart:{htmlLabels:false,useMaxWidth:false,nodeSpacing:24,rankSpacing:24,curve:'linear',padding:10}});
   await mermaid.parse(graph);
   return (await mermaid.render('flow'+id,graph)).svg;
  },{id,graph});
  fs.writeFileSync(path.join(__dirname,`flow-${id}.svg`),svg);
  const info=await sharp(Buffer.from(svg)).metadata();
  await sharp(Buffer.from(svg)).flatten({background:'#ffffff'}).resize({width:Math.round(info.width*2)}).png().toFile(path.join(__dirname,`flow-${id}.png`));
  const widthIn=Math.min(6,7.55*info.width/info.height);
  reports.push({id,width:info.width,height:info.height,widthIn,heightIn:widthIn*info.height/info.width,effectiveFontPt:22*widthIn/info.width*72});
 }
 fs.writeFileSync(path.join(__dirname,'figure-sizes.json'),JSON.stringify(reports,null,2));
 process.stdout.write(JSON.stringify(reports,null,2));
}finally{if(browser)await browser.close()}})().catch(e=>{process.stderr.write(String(e.stack||e));process.exitCode=1});
