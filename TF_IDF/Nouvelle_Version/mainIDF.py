from df_idfV2 import calc_df_idfV2


docs = ["Redbull told Max who was going last to let ALL OTHER CARS PAST!",
        "RedBull told Verstappen to let all other cars pass",
        "Strategy Redbull has him covered",
        "Max is the world champion",
        "Verstappen champion",
        "max is a cheater",
        "I love a vodka redbull",
        "Seb with a Redbull helmet hits different",
        "People need to realise it was the FIA and not max /redbull  any other driver would of taken it but the fault",
        "The true world champion",
        "Lewis Hamilton deserve the title of world champion",
        "Max Verstappen steal the world champion title",
        "Max is the new world champion"]

res = calc_df_idfV2(docs, "idf_save.csv")