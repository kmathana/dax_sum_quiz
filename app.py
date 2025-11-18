import streamlit as st

st.set_page_config(page_title="DAX: SUM vs SUMX Quiz", page_icon="📊", layout="centered")

st.title("📊 DAX Quiz: SUM vs SUMX")
st.write(
    "Test your understanding of when to use **SUM** and when to use **SUMX**. "
    "Select the best answer for each question and then check your score."
)

# Question structure
questions = [
    {
        "id": 1,
        "title": "Total manhours × cost per hr",
        "description": """
We have a table **Sales** with columns:

- `Orders[ManHrs]`  
- `WorkCenter[Cost/Hr]`  

There is **no** `Orders[ManHrsTotal]` column.  
We want: **Total Cost = Σ (ManHrs × Cost/Hr)**.  
Which measure is correct?
""",
        "options": [
            "Total Cost = SUM ( Orders[ManHrs] * WorkCenter[CostHrs] )",
            "Total Cost = SUMX ( Orders, Orders[ManHrs] * WorkCenter[Cost/Hr] )",
        ],
        "correct": 1,
        "explanations": [
            "❌ `SUM` cannot iterate row by row over an expression that multiplies two columns.",
            "✅ Correct. `SUMX` iterates each row and evaluates `ManHrs * Cost/Hr` per row."
        ]
    },
    {
        "id": 2,
        "title": "Summing an Existing Total Column",
        "description": """
We have a table **Sales** with columns:

- `Orders[ManHrs]`  
- `WorkCenters[Cost/Hr]`  
- `Orders[ManHrsTotal]` = ManHrs × Cost/Hr (already computed in source/Power Query)  

We want the grand total of `Orders[ManHrsTotal]`.  
Which is the most appropriate measure?
""",
        "options": [
            "Total Cost = SUM ( Orders[ManHrsTotal] )",
            "Total Cost = SUMX ( Orders, Orders[ManHrsTotal] )",
        ],
        "correct": 0,
        "explanations": [
            "✅ Correct. `SUM` is enough when you are just aggregating one numeric column.",
            "ℹ️ This works, but `SUMX` is unnecessary overhead here."
        ]
    },
    {
        "id": 3,
        "title": "Weighted Average Using SUMX",
        "description": """
We have a table **Grades**:

- `Grades[Score]`  
- `Grades[Weight]`  

We want the weighted average:  
**Σ(Score × Weight) ÷ Σ(Weight)**.  
Which measure correctly uses `SUMX`?
""",
        "options": [
            "Weighted Average = SUM( Grades[Score] * Grades[Weight] ) / SUM( Grades[Weight] )",
            "Weighted Average = SUMX( Grades, Grades[Score] * Grades[Weight] ) / SUM( Grades[Weight] )",
        ],
        "correct": 1,
        "explanations": [
            "❌ Wrong. `SUM` cannot correctly evaluate `Score * Weight` row by row.",
            "✅ Correct. `SUMX` iterates each row to compute `Score * Weight`."
        ]
    }
]

st.write("---")

# Store answers in session_state
if "answers" not in st.session_state:
    st.session_state.answers = {}

# Render questions
for q in questions:
    st.subheader(f"{q['id']}. {q['title']}")
    st.markdown(q["description"])

    choice = st.radio(
        "Choose one:",
        q["options"],
        index=None,
        key=f"q_{q['id']}",
        label_visibility="collapsed",
    )

    st.session_state.answers[q["id"]] = choice
    st.write("")  # spacing

if st.button("Check my answers ✅", use_container_width=True):
    correct_count = 0

    for q in questions:
        st.write("---")
        st.markdown(f"### {q['id']}. {q['title']}")
        chosen = st.session_state.answers.get(q["id"])
        correct_idx = q["correct"]

        if chosen is None:
            st.warning("You didn't select an answer for this question.")
            continue

        chosen_idx = q["options"].index(chosen)
        st.markdown(f"**Your answer:** {chosen}")

        if chosen_idx == correct_idx:
            correct_count += 1
            st.success(q["explanations"][chosen_idx])
        else:
            st.error(q["explanations"][chosen_idx])
            st.info(f"**Remember:** {q['explanations'][correct_idx]}")

    st.write("---")
    st.success(f"🎉 You got **{correct_count} / {len(questions)}** correct.")
