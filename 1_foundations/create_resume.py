from dotenv import load_dotenv
from openai import OpenAI


def write(file_name, txt):
    with open(file_name, "w") as f:
        f.write(str(txt))


def create_resume(openai):
    # create message
    messages = [
        {
            "role": "user",
            "content": "create a random name and a resume along with it.  Make sure the resume is written in first person.  Include challenges, accompolishments, hobbies, and years of experience",
        }
    ]

    # call api
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
    )

    # get content
    resume = response.choices[0].message.content

    # print to screen
    print(resume)

    return resume


def create_summary(openai, txt):
    # create message
    messages = [
        {
            "role": "user",
            "content": "summarize the following resume in just three sentences: " + txt,
        }
    ]

    # call api
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
    )

    # get content
    summary = response.choices[0].message.content

    # print to screen
    print(summary)
    return summary


def main():
    # load dotenv
    load_dotenv()

    # create client
    openai = OpenAI()

    # create resume
    bogus_resume = create_resume(openai)

    # write to file (so we don't have to call the llm to generate another resume)
    write("bogus_resume.txt", bogus_resume)

    # create summary
    bogus_summary = create_summary(openai, bogus_resume)

    # write to file (so we don't have to call the llm to generate another resume)
    write("bogus_summary.txt", bogus_summary)


if __name__ == "__main__":
    main()
