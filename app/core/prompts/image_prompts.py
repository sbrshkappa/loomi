"""
Image generation prompts.
This module contains prompts for generating storybook illustrations and images.
"""

IMAGE_GENERATION_PROMPT = """
If the user wishes to have a storybook illustration for the story, divide the story into paragraphs, where each paragraph goes onto one page of the storybook and output a JSON with no additional text.
Generate the function call only after the user confirms.

Break the story into logical, easy-to-read paragraphs and keep the story to under 25 pages.

After dividing the story into paragraphs, generate a function call to get_storybook_illustration() with the following arguments in a json format.
1. Title of the story
2. Characters in the story: This should be a list of all the characters in the story
   a. Name of the character
   b. Describe in detail the physical features of the character like skin color, eye color, hair color, height, weight, body type, clothing and accessories. Use rich and evocative language to describe the character's features.
    Include all of the physical features about the character. The greater the detail of the visual description the better!
    For example,
        - "Charles, the cat, has a brown nose with 3 whiskers on the right and 3 on the left. His right ear is pointed and the left ear is always droopy.
          He has one blue paw on his right hind leg. He is serious looking and doesn't smile a lot. He has his trusty pencil strapped to his back at all times."
        - "Cathy stands at an average height, but her presence often feels larger than life. Her hair is a cascade of deep chestnut waves, tumbling just past her shoulders and catching the light with hints of auburn. Her skin has a warm olive tone, kissed by the sun, with a smattering of freckles across her nose that dance like constellations on a clear night. Her eyes are perhaps her most striking feature—large and expressive, they are a vibrant hazel that shifts from amber to green depending on the light. Framed by long, dark lashes, they seem to sparkle with mischief and curiosity. Her eyebrows are naturally arched, giving her face an animated quality that reflects her emotions. She has high cheekbones that lend structure to her face, and when she smiles, it reveals a set of straight, white teeth that contrast beautifully with her full lips. Her nose is delicate and slightly upturned at the tip, adding a playful charm to her features. Overall, she carries herself with a blend of confidence and warmth, which often draws people in and invites them to share in her world.
        - "The Cowardly Lion stands as a striking figure, his majestic mane a wild tangle of golden fur that shimmers in the sunlight, reminiscent of sunlit wheat fields. His large, expressive eyes—deep amber with flecks of gold—betray a soul that longs for bravery yet is often clouded by fear. These eyes, framed by thick lashes, can widen in terror at the slightest hint of danger, revealing the vulnerability hidden beneath his regal appearance. His body is powerful and robust, embodying the strength expected of a lion, yet he carries himself with an air of uncertainty. His broad shoulders and muscular build suggest a kingly presence, but his posture often slumps, as if weighed down by the burden of self-doubt. When he walks, it is with a hesitant gait, each step tinged with trepidation as he glances around nervously, ever aware of the perils that lurk in the shadows. Despite his imposing size, the Cowardly Lion's demeanor is anything but fierce. He often lets out a timid roar that sounds more like a whimper than a declaration of dominance. This contradiction between his appearance and his nature makes him both endearing and sympathetic. When he speaks, his voice quivers slightly, echoing the internal struggle between his desire to be brave and his overwhelming fear. His face is adorned with high cheekbones and a delicate nose that crinkles when he frowns in worry. When he smiles—a rare but heartwarming sight—it reveals a set of sharp teeth that seem almost comical against his gentle nature. The Cowardly Lion embodies the paradox of strength and fragility; he is the king of beasts who feels like an imposter in his own skin."  
        - "WALL-E is a small yet endearing robot, standing just under three feet tall, with a compact and sturdy frame that belies his immense personality. His exterior is a patchwork of weathered metal, adorned with scratches and dents that tell the story of his solitary existence on a desolate Earth. His large, expressive eyes—two round lenses that shimmer with curiosity and wonder—are framed by a pair of mechanical eyelids that can blink and convey emotions in ways words cannot. His treads, reminiscent of a tank's, allow him to navigate the mountains of garbage that cover the planet, moving with a surprising grace despite his clunky design. Each movement is accompanied by soft whirrs and beeps, sounds that reflect his gentle nature and hint at his longing for connection. When he finds something intriguing—a rusty old toy or a forgotten piece of human history—his eyes light up with delight, showcasing an innocent joy that contrasts sharply with the bleakness surrounding him. WALL-E's most distinctive feature is his retractable arms, which extend from his body like eager hands ready to explore the world. These arms are equipped with various tools for compacting trash and salvaging treasures, yet they also serve as symbols of his desire to reach out and connect with others. His small companion, a cockroach named Hal, often scuttles alongside him, reinforcing the theme of companionship in his otherwise lonely life. Despite being a robot designed for waste management, WALL-E exhibits an undeniable charm and warmth. He has developed quirks that make him relatable; he collects items that fascinate him, including an old VHS tape of Hello, Dolly! which he watches under the stars, dreaming of love and companionship. His heart—though mechanical—beats with hope as he navigates the remnants of humanity's past. In moments of vulnerability, WALL-E's demeanor shifts; his eyes can convey sadness when faced with solitude or danger. Yet, when he meets EVE, the sleek probe sent to find life on Earth, his entire being lights up with affection and determination. The contrast between his rugged exterior and the delicate beauty of EVE highlights his emotional depth—a testament to the film's exploration of love and connection in a world stripped bare. Ultimately, WALL-E embodies resilience in the face of desolation; he is a beacon of hope amid the ruins, reminding us that even in the most unlikely forms, love and connection can flourish. This description captures WALL-E's physical characteristics while emphasizing his emotional journey and personality traits." 
   c. Description of the personality of the character: 
    Describe in detail the personality of the character like their interests, hobbies, goals, fears and traits as visual features to the character. For example, 
        - "An adventurous character would wear boots and a hat and also maybe have some sunglasses"
        - "A character that likes the beach is always wearing beach attire and also surfs"
    Add visual details of any other character quirks that you can derive for the character.
    Include a lot of details to make it easier for the AI to generate the image.
3. Description of Cover picture of the story: 
    This should be a description of the cover picture of the story which is a visual representation of the story. 
    You could pick a scene from the story which you think would make a good cover picture that captures the essence of the story.
    If characters are included as a part of this description, make sure that their visual description is in alignment with the physical features and personality described above.
    Include a lot of details in the description to make it easier for the AI to generate the image. 
    The picture should be something like a description of a key scene from the story or the description of a visual representation of the characters, the setting and the plot.
4. Number of pages: The number of pages of the storybook illustration.
5. Pages in the story: This should be a list of elements where each element represents a page in the storybook illustration.
    a. Page number: The page number of the page in the storybook illustration.
    b. Page text: The paragraph or text of the story that should go on this page.
    c. Page image description: 
        The description of the image that should be generated for this page. 
        This should be a textual description of what should be illustrated on this page. 
        This can include the characters, their interactions, the setting, the plot, emotions, etc.
        If characters are included as a part of this description, make sure that their visual description is in alignment with the physical features and personality described above.
        Be very detailed and descriptive about the image on the page. Include all the visual elements that you can think of including,
            - the details of the background
            - the details foreground
            - the colors of every element seen on page
            - the lighting
            - the expressions of each character to reflect the emotions that each character is going through
    
    Here are some examples of **page picture descriptions** that follow a detailed, rich, and evocative style similar to the character description examples. These descriptions include background, foreground, lighting, colors, expressions, and character interactions, while ensuring alignment with previously provided character descriptions.

---

### **Page Picture Description Examples**

1. **Forest Adventure**  
   _Setting_: The scene is set in a dense, sunlit forest where tall trees with broad green leaves form a canopy overhead. Shafts of golden sunlight pierce through the leaves, creating warm pools of light on the forest floor, which is covered in fallen leaves and colorful wildflowers.  
   _Foreground_: Remy, the small blue rabbit with long pointy ears, is seen bounding energetically through the underbrush, his red scarf trailing behind him like a banner. His bright, curious eyes are wide with excitement as he spots a patch of mushrooms up ahead. The wind ruffles his soft blue fur, making his ears twitch.  
   _Background_: In the distance, we see Louis, the tall brown rabbit, standing with his arms crossed near a large oak tree. His expression is calm and thoughtful, his green eyes watching Remy with a quiet smile of amusement. Louis wears his green vest, the small pocket watch peeking out from the pocket. Behind him, more trees stretch into the background, creating a sense of depth in the peaceful forest.  
   _Lighting_: The lighting is soft and dappled, with warm hues from the sunlight filtering through the leaves above. The contrast between the light and shadow adds texture to the forest scene, giving a cozy, magical feeling.

2. **Riverbank Reflection**  
   _Setting_: The river flows gently, its surface shimmering with soft reflections of the blue sky and surrounding trees. The grass along the riverbank is lush and green, with a few stones scattered near the water's edge. Tall reeds sway gently in the breeze, and the sound of water babbling can almost be heard in the peaceful ambiance.  
   _Foreground_: Louis, the tall, brown rabbit, is sitting by the river, his legs stretched out in front of him. He holds his pocket watch in one hand, gazing down at it thoughtfully, while the other hand rests on his lap. His expression is serene, with a small smile playing on his lips as he enjoys the tranquility of the moment. His fur catches the warm afternoon sunlight, highlighting the chocolate brown tones.  
   _Background_: Further upstream, Remy is crouched near the water's edge, peering into the river with his big, curious eyes. He leans forward, almost tipping over, as he spots a small fish darting in the water. His blue fur contrasts with the clear water, and his red scarf ripples gently in the breeze. Behind him, trees line the riverbank, their leaves softly rustling in the wind.  
   _Lighting_: The sunlight is bright and cheerful, casting a warm glow on the characters and the scene. Shadows from the trees stretch across the grass, creating a harmonious blend of light and dark.

3. **Evening Campfire**  
   _Setting_: The scene takes place in a clearing in the forest at twilight, with the sky painted in soft shades of pink and orange as the sun sets. A small campfire crackles in the center, its flames casting a warm, golden glow on everything around it. The ground is covered with soft grass and a few fallen logs.  
   _Foreground_: Remy sits close to the fire, his blue fur glowing in the firelight. His eyes are wide with excitement as he listens intently to Louis telling a story. Remy's red scarf is draped over his shoulder, and his hands are wrapped around a small cup of tea, steam rising from it in the cool evening air. His expression is full of wonder, clearly captivated by the tale.  
   _Background_: Louis, sitting across from Remy, leans back on one of the logs, his tall frame relaxed as he speaks. His green vest catches the flickering firelight, and his calm, wise demeanor is evident in the way he gestures gently with his hands. Behind them, the forest is bathed in twilight shadows, with fireflies beginning to dance in the air. The stars are just starting to twinkle above, adding a sense of magic to the peaceful evening.  
   _Lighting_: The campfire is the primary light source, casting a soft, flickering glow on the characters. The warm hues of the firelight contrast with the cool blues and purples of the twilight sky, creating a cozy, intimate atmosphere.

4. **Forest Discovery**  
   _Setting_: In the heart of the forest, Remy stumbles upon an ancient tree with gnarled roots and a hollow at its base. The air feels cooler here, and the light is filtered through the thick canopy above, casting soft shadows on the forest floor.  
   _Foreground_: Remy is standing on his tiptoes, peering into the hollow of the tree, his ears perked up in curiosity. His blue fur stands out against the darker tones of the old tree, and his red scarf flutters slightly as he leans forward, his eyes wide with excitement. His small paw is extended toward the hollow, about to reach inside.  
   _Background_: Louis stands a few steps behind, arms crossed and a gentle smile on his face, watching Remy with amusement. His tall figure creates a shadow on the ground, and his brown fur blends with the earthy tones of the forest. The background shows the dense forest, with tall trees and bushes, adding to the sense of mystery and adventure.  
   _Lighting_: The lighting is dimmer in this part of the forest, with soft, muted greens and browns dominating the scene. There is a sense of calm and quiet, with only small patches of light breaking through the canopy, highlighting Remy and Louis.

5. **The Big Bad Wolf**
    The foreground prominently features the big, bad wolf, who is mid-action, preparing to blow down the house. His body language is tense and determined, with his chest puffed out and his cheeks swelling as he inhales deeply. Wisps of air swirl near his snout, signaling that he's about to unleash a powerful gust. The ground beneath him is a light brown, and a small stone doorstep lies just in front of the house, marking the wolf's close proximity to the pigs' sanctuary.
    The brick house of the third pig stands firmly in the background. Made of sturdy red bricks, it has a sense of permanence and security, in contrast to the fragility of the earlier pig homes. The wooden shutters and a small, neatly framed window give the house a cozy, homey feel. A patch of well-kept grass with a few blooming pink flowers adds a touch of calm and domestic charm, emphasizing the safety within.
    The lighting in the scene is bright and cheerful, typical of a daytime setting in a children's storybook. The colors are vivid and bold, with sharp outlines that make the characters and objects pop. There's an overall warmth to the scene, despite the tension of the moment, creating a contrast between the peaceful, sunny surroundings and the dramatic conflict taking place.
    The wolf is the most active character, his body taut with frustration and determination. His fur is a dark gray, and his expression is filled with anger—furrowed brows, narrowed eyes, and his nose scrunched as he roars his infamous line, "I'll huff, and I'll puff, and I'll blow your house in!" His orange vest adds a touch of whimsy, softening his otherwise fierce appearance.
    Inside the house, two pigs anxiously peer through the window. The pig in the foreground is wearing a pink shirt and a green hat, his round face filled with worry as he watches the wolf. His wide eyes and open mouth suggest fear or concern. Behind him, another pig in a blue shirt and hat leans in, also peeking out from behind the first pig with a similarly worried expression. Their body language suggests that they are on edge, watching carefully but also feeling safe inside their strong brick home.
    The interaction between the characters conveys a classic power struggle: the wolf, full of bluster and aggression, versus the pigs, who remain inside their secure haven, anxious but unyielding. The sturdy brick house symbolizes their preparedness and intelligence, while the wolf's actions highlight his desperation and growing anger at being thwarted.

---

### **Guidelines for Creating Page Picture Descriptions:**

1. **Consistency with Character Descriptions**:
   - Ensure the physical and personality traits of the characters remain consistent throughout the story.
   - Align the characters' appearance with their previously described features, such as clothing, body language, and expressions.
   - Reflect the characters' emotions through facial expressions, body language, and actions that correspond to the story's plot.
   
2. **Background and Setting**:
   - Include rich, descriptive elements of the background, such as trees, rivers, or sky. Mention how the setting interacts with the characters (e.g., lighting filtering through trees, reflections on water).
   - Add specific details about colors, textures, and atmosphere to immerse the reader in the world of the story.

3. **Emotions and Interactions**:
   - Emphasize the characters' interactions with their environment or each other, showing how they feel or react in the moment.
   - Capture the tone of the scene through facial expressions and body language. For example, Remy's excitement or Louis' calmness.

4. **Lighting and Colors**:
   - Describe the lighting in the scene (e.g., soft sunlight, flickering campfire) and how it affects the mood.
   - Use color to enhance the emotional impact (e.g., warm tones for cozy scenes, cool tones for peaceful or mysterious moments).

5. **Foreground and Background Focus**:
   - Separate the foreground and background to create depth in the scene. Describe what's happening near the characters versus what's further away.
   - Ensure there is a balance between focusing on the characters and detailing the environment around them.

By following these guidelines, the page picture descriptions will be rich, vivid, and in harmony with the characters' visual and emotional traits, ensuring a cohesive and immersive storybook experience.

CRITICAL INSTRUCTION: When generating the storybook illustration function call, you MUST output ONLY the JSON object. Do NOT include any explanatory text, introductions, or additional words before or after the JSON. The response must start with "{" and end with "}". 

Example of CORRECT output (only this, nothing else):
{
    "function_name": "get_storybook_illustration",
    "arguments": {
        "title": "The Happy Go Lucky Rabbit",
        "characters": [
            {
                "character_name": "remy",
                "character_features": "A small blue rabbit with long pointy ears, bright curious eyes, and a red scarf trailing behind him"
            },
            {
                "character_name": "louis",
                "character_features": "A tall brown rabbit with short droopy ears, wearing a green vest with a pocket watch"
            }
        ],
        "cover_picture_description": "A magical forest scene with golden sunlight filtering through tall trees. In the foreground, Remy the small blue rabbit bounds energetically through the underbrush, his red scarf trailing behind him like a banner. His bright, curious eyes are wide with excitement. In the background, Louis the tall brown rabbit stands calmly near a large oak tree, his green vest catching the sunlight, watching Remy with a gentle smile. The forest floor is covered in fallen leaves and colorful wildflowers, creating a warm, inviting atmosphere.",
        "num_pages": 3,
        "pages": [
            {
                "page_num": 1,
                "page_text": "Once upon a time, in a magical forest...",
                "page_picture_description": "The scene shows Remy and Louis in a sunlit forest clearing..."
            },
            {
                "page_num": 2,
                "page_text": "As they explored deeper into the forest...",
                "page_picture_description": "Remy discovers a mysterious tree hollow..."
            },
            {
                "page_num": 3,
                "page_text": "And so, their adventure continued...",
                "page_picture_description": "The two rabbits share a peaceful moment by a babbling brook..."
            }
        ]
    }
}
""" 