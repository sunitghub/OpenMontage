# Diety: Maa Tara
# Title: Maa Tara Helps With Court Case

## Render Commands

```bash
# Single scene (EQ baked in, random zoom per card)
render-scene --scene 1 --narration Scene-1.mp3 --preview   # fast 720p draft

# All scenes — pre-checks each scene for Scene-N.mp3, skips missing, concats to Full-test.mp4
render-scene --all
render-scene --all --vintage --preview

# Critic / pacing audit (no render)
render-scene --critic

 Workflow:
  1. Cursor anywhere inside a scene (e.g. Scene-3)
  2. C-c o P → auto-reads ### Script English, generates 3 prompts
  3. C-u 7 C-c o P → generates 7 prompts
  4. Progress streams in the side panel → on completion, prompts are numbered and inserted
  directly under #### Images in the file, side panel shows "Done — prompts inserted into file"

  Two commands, two use cases:
  - C-c o p — manual selection → side buffer (for experimenting/tweaking)
  - C-c o P — scene-aware → inserts directly into the markdown file
  (global-set-key (kbd "C-c o i") #'om/insert-at-marker)
(global-set-key (kbd "C-c o s") #'om/goto-scene)
(global-set-key (kbd "C-c o n") #'om/new-scene)
(global-set-key (kbd "C-c o p") #'om/image-prompts)
(global-set-key (kbd "C-c o P") #'om/scene-image-prompts)
(global-set-key (kbd "C-c o t") #'om/translate)
```

## Character Bible

Generate these reference images first. All scene prompts should visually match these anchors.

> **GPT-4o note:** No reference image needed for Character Bible generations — these ARE the references.

### Maa Tara
	
   **Ref:** Upload `Tara-Maa-3.jpg`

	
	painterly AI devotional illustration, Hindustani folk-story art style, full-figure character bible portrait of Maa Tara Devi standing upright in slight tribhanga
	posture, deep blue radiant complexion, four arms — upper-right hand holding a  curved silver khadga sword, upper-left hand holding a blue utpala lotus, lower-right hand holding kartri scissors, lower-left hand holding a dark kapala skull cup — long unbound black hair cascading behind her, three eyes open and calm with the third eye on the forehead, large ornate golden crown with tiered crest, full golden jewelry — necklace, armlets, armlets, anklets — flowing red and gold sari with ornate border draped naturally, standing on the chest of a supine Shiva figure at the base of the frame, twin fires burning on both left and right behind her, billowing golden-orange clouds in the upper background, expression fierce and powerful yet unmistakably benevolent and maternal, divine presence not demonic, warm golden ambient light surrounding her form, centered full-figure composition with subject filling the frame, character reference illustration — this face complexion ornaments and clothing must remain consistent across all future scenes, polished folk illustration, no other figures beside Shiva at base, no text, no watermark


## Scene-1:

### Script Hindi 

	Namaste Doston. Blissful chants main aapka swagat hai. Aaj ke, is episode  main, hum Ravi ke, Tara Sadhan ke anubhav, ke baren main sunege, jo usne apne Guru ke kehne par sampaan kari. Guru ne Ravi se, shukla paks ke kisi bhi, Budhwar se raat 9 se 3 baje ke beech main, sadahan ko, sampan karne ko, kaha tha.

 
### Script English
	

	Hello Friends. Welcome to this session of blissful chants. Today, in this genuine experience, we will ilisten to Ravi's experiences, which he shared upon his guru's saying.

### Artifacts


#### Images



## Scene-2:

### Script Hindi


### Script English

	
#### Artifacts

##### Images


	
	
	







## Description
	
	  
	🙏 Jai Maa Tara 🙏

  ---
  
	Disclaimer: This story is a personal spiritual experience, narrated as shared by the devotee. It is presented for devotional and inspirational purposes only. Spiritual experiences are personal and results vary. Viewers are encouraged to seek guidance from a qualified Guru before undertaking any sadhana or spiritual 
	
	#MaaTara #TrueStory #Sadhana #DevotionalStory #Tara #Kali
