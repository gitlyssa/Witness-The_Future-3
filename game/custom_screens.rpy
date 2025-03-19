screen inventory_button:
    hbox:
        xpos 0 ypos 0.036
        imagebutton:
            auto "inventory-icon-%s" at Transform(zoom=0.5)
            action ToggleScreen("inventory")
        
        imagebutton:
            auto "cases-%s" at Transform(zoom=0.5)
            action [Hide("inspectItem"), ToggleScreen("case_description")]

screen case_description:
    image "menu-bg_1" align (0.5, 0.15) at Transform(zoom=0.65)
    if persistent.case_choice == "Case A":
        $ item_name = "Case A"
        $ item_desc = "Case A description"
        $ case_image = "CaseA_File.png"
    else:
        $ item_name = "Case B"
        $ item_desc = "Case B desciption"
        $ case_image = "CaseB_File.png"
    text "{}".format(item_name) size 30 align (0.35, 0.62) color "#000000"
    text "{}".format(item_desc) size 30 align (0.63, 0.35) color "#000000"
    image "[case_image]" align (0.3, 0.4) at Transform(zoom=2)

screen reminder:
    hbox:
        xpos 0.8 ypos 0.615
        imagebutton:
            auto "question_%s" at Transform(zoom=0.3)
            action ToggleVariable("reminder_pressed")

    $ reminder_text = responses[-1] if answered_first_question else ai_first_question
    
    showif reminder_pressed:
        add "reminder pop up" at Transform(xalign=0.5, yalign=0, zoom=0.9, xzoom=0.86)

        frame:
            xalign 0.5
            xsize 1400  # Set width to control text margins
            yalign 0.1
            background None

            text "[reminder_text]":
                xalign 0.5
                text_align 0.5  # Center align text within the frame
                size 35  # Adjust font size as needed
                color "#ffffff"  # Adjust text color as needed
                xmaximum 1300


screen prefix_dropdown():
    modal True
    zorder 999

    frame:
        background "#202020"
        xalign 0.53
        yalign 0.545
        padding (10, 10)

        vbox:
            spacing 5
            for option in ["Mr.", "Ms.", "Mrs.", "Mx.", "Dr."]:
                textbutton option:
                    action [SetVariable("player_prefix", option), Hide("prefix_dropdown")]

screen nameyourself():
    default p_first_name_input = VariableInputValue("player_fname", default=False)
    default p_last_name_input = VariableInputValue("player_lname", default=False)
    add "frame" at Transform(zoom=0.6, xalign=0.5, yalign=0.45)

    frame:
        left_padding 20
        right_padding 20
        xalign 0.5
        yalign 0.3
        background None
        text "Enter your first and last name.":
            xalign 0.5
            yalign 0.3

    vbox:
        xalign 0.5
        yalign 0.48

        text "Prefix (Dr./Mx./Mr./Ms./Mrs.):"
        hbox:
            button:
                background "#4c4c4cd0"
                xsize 200
                action Show("prefix_dropdown", transition=dissolve)
                text "[player_prefix]" xalign 0.5
            textbutton "∇":
                background "#4C4C4C"
                action Show("prefix_dropdown", transition=dissolve)

        text "First Name: "
        button:
            background "#4c4c4cd0"
            xsize 300
            action p_first_name_input.Toggle()
            input:
                pixel_width(500)
                value p_first_name_input
        text "Last Name: "
        button:
            background "#4c4c4cd0"
            xsize 300
            action p_last_name_input.Toggle()
            input:
                pixel_width(1000)
                value p_last_name_input

    hbox:
        xalign 0.6
        yalign 0.7
        textbutton "Done":
            style "selection_button"
            text_color "#ffffff"
            # background "#4C4C4C"
            # hover_background "#363737"
            action Jump("lex_intro2")
            sensitive (player_fname.strip() and player_lname.strip() and player_prefix.strip())

screen case_a_screen:
    add "frame" at Transform(zoom=0.85, xalign=0.5, yalign=0.3)
    frame:
        xpadding 40
        ypadding 20
        xalign 0.5
        yalign 0.2
        ysize 300
        xsize 1010
        background None
        text "On the night of March 15th, Ana Konzaki was found dead at a house party hosted by her and her boyfriend, Ezra Verhoesen. The party was a casual gathering with alcohol and marijuana present, but no hard drugs. Witnesses report that a violent altercation broke out between Ezra and an unknown individual, resulting in both men sustaining injuries.\n\nAna was later discovered unconscious with a fatal head wound. One witness claims to have called a drug dealer, Edward Bartlett, on the night of the party. Edward is also the accused on trial, as some witnesses identified him as the individual who attacked Ezra in a lineup."
  
    hbox:
        xalign 0.48
        yalign 0.75
        spacing 100

        button:
            # background "#4C4C4C"
            # hover_background "#363737"
            style "selection_button"
            action [Jump("case_selection_menu"), SetVariable("persistent.case_choice", None)]
            text "Return to Case Selection"

        button:
            # background "#4C4C4C"
            # hover_background "#363737"
            style "selection_button"
            action [SetVariable("persistent.case_choice", "Case A"), If(tutorial_skipped or switch_cases, Jump("specialty_menu"), Jump("tutorial_specialty"))]
            text "Choose Case A"

screen case_b_screen:
    add "frame" at Transform(zoom=0.85, xalign=0.5, yalign=0.3)
    frame:
        xpadding 40
        ypadding 20
        xalign 0.5
        yalign 0.2
        ysize 300
        xsize 1000
        background None
        text "An unknown body was discovered floating in a lake in a public park by a passer-by. The victim was later identified by family as 13 year old Jacob DeSouza. The cause of death appears to be strangulation, and not drowning. The accused is his adoptive father, Kiernan DeSouza.\n\nKiernan had been reported absent from work and was not at home around the time of Jacob's death. Furthermore, Kiernan's car was discovered near the lake where the body was found. The investigation has been complicated by the lack of direct witnesses and evidence of forced entry into the home."

    hbox:
        xalign 0.48
        yalign 0.75
        spacing 100

        button:
            # background "#4C4C4C"
            # hover_background "#363737"
            style "selection_button"
            action [Jump("case_selection_menu"), SetVariable("persistent.case_choice", None)]
            text "Return to Case Selection"

        button:
            # background "#4C4C4C"
            # hover_background "#363737"
            style "selection_button"
            action [SetVariable("persistent.case_choice", "Case B"), If(tutorial_skipped or switch_cases, Jump("specialty_menu"), Jump("tutorial_specialty"))]
            text "Choose Case B"

screen specialty_exploration_screen(specialty): 
    $ case_details = cases[persistent.case_choice]
    $ evidence_dict = case_details['evidence'][specialty] 

    add "frame" at Transform(zoom=0.85, xalign=0.5, yalign=0.3)
    
    frame:
        xpadding 40
        ypadding 20
        xalign 0.5
        yalign 0.2
        ysize 500
        xsize 1300
        background None

    text "[case_details['case_name']]\nSpecialty: [specialty]":
        xalign 0.5
        yalign 0.2

    text "Evidence Point 1: [evidence_dict['point_1']]\n\nEvidence Point 2: [evidence_dict['point_2']]":
        xalign 0.5
        yalign 0.42
        xmaximum 1200

    hbox:
        xalign 0.5
        yalign 0.7
        spacing 100

        button:
            # background "#4C4C4C"
            # hover_background "#363737"
            style "selection_button"
            action Jump("specialty_menu")
            text "Return to Specialty Selection"

        button:
            # background "#4C4C4C"
            # hover_background "#363737"
            style "selection_button"
            action [SetVariable("persistent.specialty", specialty), If(tutorial_skipped == False, Jump("tutorial_lex_diff"), Jump("difficulty_selection"))]
            text "Choose this Specialty"

screen evaluation_screen:
    modal True  
    frame:
        xalign 0.5
        yalign 0.5
        xsize 800  
        ysize 600  
        background "#222"  

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            text "Evaluation":
                color "#FFF"
                size 32
                xalign 0.5
 
            viewport:
                xsize 700
                ysize 400
                scrollbars "vertical"
                mousewheel True
                text renpy.store.eval_comments: 
                    color "#FFF"
                    size 16
                    xalign 0.5
            
            text "Total Score: [renpy.store.score]/100": 
                color "#FFF"
                size 24
                xalign 0.5
            
        textbutton "Done":
            background "#4C4C4C"
            hover_background "#363737"
            xalign 0.9
            yalign 0.9
            action Jump("ending_0")

screen credits_lol:
    frame:
        xalign 0.5
        yalign 0.5
        xsize 800  
        ysize 600  
        background "#222"  

        vbox:
            xalign 0.5
            yalign 0.5

            text "THANKS FOR PLAYING":
                color "#FFF"
                size 32
        hbox:
            xalign 0.5
            yalign 0.7
            #spacing 100
            button:
                background "#4C4C4C"
                hover_background "#363737"
                action [SetVariable("answered_first_question", False), Jump("start")]
                text "Try again"
#           button:
#               background "#4C4C4C"
#               hover_background "#363737"
#               action [SetVariable("LEX_DIFFICULTY", specialty), Jump("interview_loop")]
#               text "Testify for the [unplayed_difficulty]"

screen darken_background():
    # Dark transparent layer
    add Solid("#000000a3")  # Black with 50% opacity

style selection_button:
    background "#68c5e1"  
    hover_background "#5092a6"
    insensitive_background "#2a2a2a"
    padding (40, 12)

screen achievement_banner(text):
    zorder 100
    frame:
        xpos 12
        ypos -100
        at slide_in
        xsize 400
        ysize 100
        background "#6bc0d0cc"

        text text size 30 color "#ffffff" xalign 0.5 yalign 0.5

    timer 3.0 action Hide("achievement_banner")

transform slide_in:
    ypos 20
    easein 0.5 ypos 50  # Smooth slide-down effect

