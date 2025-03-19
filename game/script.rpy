﻿define l = Character("Lex Machina")
define s = Character(name=("Nina"), image="nina")
define j = Character("Judge")

default player_fname = "" 
default player_lname = ""
default player_prefix = ""
default reminder_pressed = False
default answered_first_question = False
default switch_cases = False

label start:
    scene bg spec
    # REQUIRED FOR INVENTORY:
    $config.rollback_enabled = False # disables rollback
    $quick_menu = False # removes quick menu (at bottom of screen) - might put this back since inventory bar moved to right side
    
    # environment:
    $environment_SM = SpriteManager(event = environmentEvents) # sprite manager that manages environment items; triggers function environmentEvents() when event happens with sprites (e.g. button click)
    $environment_sprites = [] # holds all environment sprite objects
    $environment_items = [] # holds environment items
    $environment_item_names = [] # holds environment item names
    
    # inventory
    $inventory_SM = SpriteManager(update = inventoryUpdate, event = inventoryEvents) # sprite manager that manages evidence items; triggers function inventoryUpdate 
    $inventory_sprites = [] # holds all evidence sprite objects
    $inventory_items = [] # holds evidence items
    $inventory_item_names = ["Fingerprint", "Handprint", "Gin", "Splatter", "Footprint"] # holds names for inspect pop-up text 
    $inventory_db_enabled = False # determines whether up arrow on evidence hotbar is enabled or not
    $inventory_ub_enabled = False # determines whether down arrow on evidence hotbar is enabled or not
    $inventory_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for evidence bar
    $inventory_slot_padding = 120 / 2 # sets padding size between evidence slots
    $inventory_first_slot_x = 105 # sets x coordinate for first evidence slot
    $inventory_first_slot_y = 300 # sets y coordinate for first evidence slot
    $inventory_drag = False # by default, item isn't draggable

    # toolbox:
    $toolbox_SM = SpriteManager(update = toolboxUpdate, event = toolboxEvents) # sprite manager that manages toolbox items; triggers function toolboxUpdate 
    $toolbox_sprites = [] # holds all toolbox sprite objects
    $toolbox_items = [] # holds toolbox items
    # $toolbox_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolbox_db_enabled = False # determines whether up arrow on toolbox hotbar is enabled or not
    $toolbox_ub_enabled = False # determines whether down arrow on toolbox hotbar is enabled or not
    $toolbox_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for toolbox bar
    $toolbox_slot_padding = 120 / 2 # sets padding size between toolbox slots
    $toolbox_first_slot_x = 105 # sets x coordinate for first toolbox slot
    $toolbox_first_slot_y = 300 # sets y coordinate for first toolbox slot
    $toolbox_drag = False # by default, item isn't draggable

    # toolbox popup:
    $toolboxpop_SM = SpriteManager(update = toolboxPopUpdate, event = toolboxPopupEvents) # sprite manager that manages toolbox pop-up items; triggers function toolboxPopUpdate
    $toolboxpop_sprites = [] # holds all toolbox pop-up sprite objects
    $toolboxpop_items = [] # holds toolbox pop-up items
    # $toolboxpop_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolboxpop_db_enabled = False # determines whether up arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_ub_enabled = False # determines whether down arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for toolbox pop-up bar
    $toolboxpop_slot_padding = 120 / 2 # sets padding size between toolbox pop-up slots
    $toolboxpop_first_slot_x = 285 # sets x coordinate for first toolbox pop-up slot
    $toolboxpop_first_slot_y = 470 # sets y coordinate for first toolbox pop-up slot
    $toolboxpop_drag = False # by default, item isn't draggable

    $current_scene = "scene1" # keeps track of current scene
    
    $dialogue = {} # set that holds name of character saying dialogue and dialogue message
    $item_dragged = "" # keeps track of current item being dragged
    $mousepos = (0.0, 0.0) # keeps track of current mouse position
    $i_overlap = False # checks if 2 inventory items are overlapping/combined
    $ie_overlap = False # checks if an inventory item is overlapping with an environment item

    # show screen inventory 

label setupScene1:

    # --------- ADDING ENVIRONMENT ITEMS ---------
    #$environment_items = ["lid"]

    python:
        # --------- ADDING ITEMS TO INVENTORY --------- 
        # change these parameters as necessary
        addToInventory(["fingerprint", "handprint", "gin", "splatter", "footprint"])

        for item in environment_items: # iterate through environment items list
            idle_image = Image("Environment Items/{}-idle.png".format(item)) # idle version of image
            hover_image = Image("Environment Items/{}-hover.png".format(item)) # hover version of image
    
            t = Transform(child= idle_image, zoom = 0.5) # creates transform to ensure images are half size
            environment_sprites.append(environment_SM.create(t)) # creates sprite object, pass in transformed image
            environment_sprites[-1].type = item # grabs recent item in list and sets type to the item
            environment_sprites[-1].idle_image = idle_image # sets idle image
            environment_sprites[-1].hover_image = hover_image # sets hover image

            # --------- SETTING ENV ITEM WIDTH/HEIGHT AND X, Y POSITIONS ---------
            
            # NOTE: for each item, make sure to set width/height to width and height of actual image
            # if item == "lid":
            #     environment_sprites[-1].width = 300 / 2
            #     environment_sprites[-1].height = 231 / 2
            #     environment_sprites[-1].x = 1000
            #     environment_sprites[-1].y = 500
        
    # scene scene-1-bg at half_size - sets background image

    $ persistent.case_choice = None
    $ persistent.specialty = None
    $ tutorial_skipped = False
    $ context_history = []
    $ unintelligible_count = 0
    $ mentioned_truths = set()  

    show nina normal3
    s "Welcome to the courtroom. My name is |Supervisor|, and I'll be guiding you through your preparation before you deliver expert testimony!"
    s "Would you like me to go through the tutorial? Or should we get straight to case selection?"
    hide nina normal3

    menu:
        s "Would you like me to go through the tutorial? Or should we get straight to case selection?"
        "Let's do the tutorial first.":
            jump tutorial_start
        "Let's get straight to case selection!":
            $ tutorial_skipped = True
            jump case_selection_menu

label tutorial_start:
    show nina normal1
    s "Don't worry, this is not a real court, and there currently are no stakes involved. It is simply a training simulation intended to help you practice!"
    show nina normal2
    s "Let's start by selecting your case. Each one will present different forensic challenges, so read through the case details carefully before making your choice."
    jump case_selection_menu

label case_selection_menu:
    scene bg spec
    menu:
        "Case A: The Death of Ana Konzaki":
            call screen case_a_screen

        "Case B: The Park Incident":
            call screen case_b_screen
    return

label tutorial_specialty:
    scene bg spec
    show nina normal3
    s "Perfect! Now, let's choose your forensic specialty."
    show nina normal2
    s "As an expert witness, your role is to analyze and present evidence within your area of expertise. Your selection will determine the type of evidence you'll be responsible for in court."
    show nina thinknote1
    s "Because this is just a mock scenario, you will only have to testify for two pieces of evidence. Please look through the evidence carefully!"
    jump specialty_menu

label specialty_menu:
    scene bg spec
    $ chosen_specialty = None
    menu:
        "Anthropology":
            $ chosen_specialty = "Anthropology"
            jump specialty_exploration
        "Biology":
            $ chosen_specialty = "Biology"
            jump specialty_exploration
        "Chemistry":
            $ chosen_specialty = "Chemistry"
            jump specialty_exploration
        "Psychology":
            $ chosen_specialty = "Psychology"
            jump specialty_exploration
        "Identification":
            $ chosen_specialty = "Identification"
            jump specialty_exploration
        "Switch cases":
            $ switch_cases = True
            jump case_selection_menu

label specialty_exploration:
    $ case_details = cases[persistent.case_choice]
    call screen specialty_exploration_screen(chosen_specialty)

label tutorial_lex_diff:
    scene bg spec
    show screen inventory_button
    show nina normal3
    show screen darken_background
    s "Great choice! On the top left corner, you'll see the evidence button. If you want to view all your evidence, click on it!"
    s "If you want more information about a particular piece of evidence, press on the info button when hovering over one."
    hide screen darken_background
    s "Now, there's just one more thing before you step into court."
    show nina normal2
    s "Inside the courtroom, you'll be examined by Lex Machina, a mock trial lawyer."
    show nina write1
    s "Depending on your selection, Lex will take on one of two roles—either as the prosecution or the defense."
    show nina thinknote1
    s "If you choose prosecution, Lex will act as the Crown attorney. This is the easier option." 
    s "As a prosecutor, Lex's goal is to establish the truth and ensure your testimony is clear, credible, and useful to the court. In this difficulty, if you miss something important, Lex may prompt you to clarify or expand on your findings."
    show nina normal2
    s "If you choose defense, Lex will act as the defense attorney. This is the harder option."
    show nina normal1
    s "A defense lawyer's priority is to protect their client, which means they will work to discredit you and your testimony. Expect Lex to challenge you with leading or loaded questions, and other cross-examination techniques designed to undermine your credibility." 
    s "You'll need to stay composed, justify your conclusions, and ensure your testimony remains admissible."
    show nina normal3
    s "Choose wisely! Your decision will shape the difficulty of your examination."
    show nina thinknote1
    s "Once you've made your selection, the court room awaits! I'll be seeing you after your trial. Good luck!"
    jump difficulty_selection 

label difficulty_selection:
    scene bg spec
    menu:
        "Prosecution":
            $ LEX_DIFFICULTY = "prosecution"
            $ unplayed_difficulty = "defense"
            show screen inventory_button
            jump lex_intro
        "Defense":
            $ LEX_DIFFICULTY = "defense"
            $ unplayed_difficulty = "prosecution"
            show screen inventory_button
            jump lex_intro

    label lex_intro:
        scene bg interview
        "A figure walks into the room, wearing a crisp suit and carrying a briefcase."
        show lawyer
        l "Hello, my name is Lex Machina. I'll be examining you as an expert witness for this case."
        l "Could you please state your first and last name for the court?"
        hide lawyer
        hide screen inventory_button
        hide screen inventory
        hide screen inspectItem
        hide screen case_description
        call screen nameyourself

    label lex_intro2:
        show screen inventory_button
        show lawyer
        l "Thank you, [player_prefix] [player_lname]." 
        l "Before we start, let me introduce you to the Judge presiding over this case, |judge name|."
        show judge
        j "Nice to meet you, [player_prefix] [player_lname]! Since this is not a real case, I will not be making any verdicts today, but I will be evaluating your testimony with Lex."
        hide judge
        show lawyer
        l "I believe you've chosen to testify as an expert for [persistent.case_choice] in [persistent.specialty]. Very well, let's proceed."
    $ case_details = cases[persistent.case_choice] 
    $ ai_first_question = generate_response("Generate the first question for the expert witness to establish qualification in their field. Keep it short.", player_prefix, player_fname, player_lname, persistent.specialty, case_details, context_history, unintelligible_count,)
    jump first_question

label first_question:
    $ responses = split_string(ai_first_question)
    $ say_responses(responses)
    $ context_history.append(f"AI: {ai_first_question}")
    show screen reminder
    $ user_prompt = renpy.input("Your answer here:")
    $ context_history.append(f"User: {user_prompt}")
    python:
        all_truths = create_all_truths_set(persistent.case_choice, persistent.specialty)
    $ ai_response = generate_response(user_prompt, player_prefix, player_fname, player_lname, persistent.specialty, case_details, context_history, unintelligible_count)
    $ responses = split_string(ai_response)
    hide screen reminder
    $ reminder_pressed = False
    $ say_responses(responses)
    $ context_history.append(f"AI: {ai_response}")

    if "QUALIFICATION: UNQUALIFIED" in ai_response:
        jump game_over
    elif "QUALIFICATION: QUALIFIED" in ai_response:
        $ mentioned_truths = set()
        $ answered_first_question = True
        python:
            for evidence_point in truth_bases[persistent.case_choice][persistent.specialty]:
                for truth in truth_bases[persistent.case_choice][persistent.specialty][evidence_point]:
                    if truth.lower() in user_prompt.lower():
                        mentioned_truths.add(truth.lower())
        show screen achievement_banner("The court finds you qualified!")
        jump interview_loop
    elif "unintelligible response" in ai_response:
        $ unintelligible_count += 1
        if unintelligible_count >= 3:
            jump game_over
        else:
            jump first_question
    else:
        "An unexpected error occurred. Please restart the game."
        return

label interview_loop:
    while True:
        show screen reminder
        $ user_prompt = renpy.input("Your answer here:")
        if user_prompt.lower() in ["exit", "quit", "stop"]:
            l "Thank you for your time, [player_prefix] [player_lname]. This concludes the interview."
            return
        $ context_history.append(f"User: {user_prompt}")
        python:
            all_truths = create_all_truths_set(persistent.case_choice, persistent.specialty) 
            for evidence_point in truth_bases[persistent.case_choice][persistent.specialty]:
                for truth in truth_bases[persistent.case_choice][persistent.specialty][evidence_point]:
                    if truth.lower() in user_prompt.lower():
                        mentioned_truths.add(truth.lower()) 

        $ ai_response = generate_response(user_prompt, player_prefix, player_fname, player_lname, persistent.specialty, case_details, context_history, unintelligible_count)
        $ responses = split_string(ai_response)
        $ reminder_pressed = False
        hide screen reminder
        $ reminder_pressed = False
        $ say_responses(responses)
        $ context_history.append(f"AI: {ai_response}")

        python:
            if "i have no further questions, your honour" in ai_response.lower(): 
                renpy.jump("interview_end")

        if "QUALIFICATION: UNQUALIFIED" in ai_response:
            jump game_over
        if "unintelligible response" in ai_response:
            $ unintelligible_count += 1
            if unintelligible_count >= 3:
                jump game_over
            elif "examination cannot continue" in ai_response.lower():
                jump game_over
            else:
                $ ai_response = generate_response("Generate a question for the user. Ensure that they follow the rules of the court and establish key information for the triers of fact.", player_prefix, player_fname, player_lname, persistent.specialty, case_details, context_history, unintelligible_count)
                $ responses = split_string(ai_response)
                $ say_responses(responses)
                $ context_history.append(f"AI: {ai_response}")
                jump interview_loop
        else:
            $ unintelligible_count = 0
    return

label game_over:
    scene bg gameover
    "The examination has been terminated because you were deemed unqualified to testify as an expert witness."
    "Please select \"Restart\" to try again."
    menu:
        "Restart":
            $ answered_first_question = False
            jump start
        "Quit":
            $ renpy.quit()

python:
    if LEX_DIFFICULTY == "prosecution":
        unplayed_difficulty = "defense"
    elif LEX_DIFFICULTY == "defense":
        unplayed_difficulty = "prosecution"
    else:
        unplayed_difficulty = "error"

label interview_end:
    scene bg interview
    show lawyer
    l "Thank you for your time, [player_prefix] [player_lname]."
    show judge
    j "Thank you, Lex. [player_prefix] [player_fname] [player_lname], you may leave the court room. You will receive your evaluation outside with your supervisor."
    hide judge
    hide lawyer
    python:
        try:
            all_truths = create_all_truths_set(persistent.case_choice, persistent.specialty)
            full_transcript = "\n".join(context_history)
            evaluation_prompt = (
                f"Evaluate the expert witness testimony based on the following transcript:\n\n{full_transcript}\n\n"
                f"The expert testified as a {persistent.specialty} in {case_details['case_name']}.\n\n"
                f"All the truth bases they needed to say are:\n\n{all_truths}\n\n"
                f"Evaluate the testimony considering these grading criteria in mind:\n\n{grading_criteria}\n\n"
                f"Generate 3-5 bullet points that explain the evaluation and give a total score out of 100 based on the grading criteria by saying exactly 'Score: X'. Try to use the user's exact words to explain why you have your feedback."
            )
            evaluation_response = generate_response(evaluation_prompt, player_prefix, player_fname, player_lname, persistent.specialty, case_details, context_history, unintelligible_count)
            score_match = re.search(r"Score: (\d+)", evaluation_response)
            if score_match:
                score = int(score_match.group(1))
                eval_comments = re.sub(r"Score: \d+", "", evaluation_response).strip()
            else:
                score = 0
                eval_comments = "Score not found in evaluation."

            renpy.store.eval_comments = evaluation_response
            renpy.store.score = score  

            print(f"EVAL COMMENTS:\n{renpy.store.eval_comments}")
            print(f"SCORE:\n{renpy.store.score}")

        except Exception as e:
            renpy.store.eval_comments = f"Error: {str(e)}"
            renpy.store.score = 0

    scene bg spec
    show sprite happy
    s "Welcome back, [player_fname]! In just a second, Lex and the Judge will return with any feedback they have for you."
    show sprite explain
    s "After you receive your feedback, I encourage you to testify again for the [unplayed_difficulty] to get the full court room experience."
    show sprite neutral
    s "You can also choose a whole new case and specialty and start again! The choice is yours!"
    #ADD FOOTSTEPS SOUND HERE HEHEHE
    show sprite think
    s "Oh! Sounds like Lex and the Judge are about to join us. Don't worry, I'm sure you did great!"
    jump evaluation_sec

label evaluation_sec:
    scene bg spec
    show lawyer
    l "Hello, |supervisor|. [player_prefix] [player_lname], are you ready to receive your evaluation?"
    hide lawyer
    call screen evaluation_screen                                                                                

label ending_0:
    scene bg spec
    call screen credits_lol
