# import json
# import yt_dlp

# URL = 'https://www.youtube.com/watch?v=rjE4XgsqyxE'

# ydl_opts = {
#     'format': 'm4a/bestaudio/best',
#     # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
#     'postprocessors': [{  # Extract audio using ffmpeg
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'm4a',
#     }]
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     error_code = ydl.download(URL)

# ydl_opts = {
#     "format": "bestaudio/best",
#     "outtmpl": tmp_filename,
#     "quiet": True,
#     "noplaylist": True,
# }

# import whisper

# model = whisper.load_model("base")
# result = model.transcribe("file.m4a")
# print(result["text"])


from google import genai
from google.genai import types
from decouple import config
API_KEY = config('GEMINI_API_KEY')

client = genai.Client(
    api_key= API_KEY,
    http_options=types.HttpOptions(api_version='v1alpha')
)

# response = client.models.generate_content(
#     model='gemini-2.0-flash-001', contents='Why is the sky blue?'
# )
# print(response.text)


prompt = """Based on the following transcript, generate a quiz in valid JSON format.

The quiz must follow this exact structure:

{{
  "title": "Create a concise quiz title based on the topic of the transcript.",
  "description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",
  "questions": [
    {{
      "question_title": "The question goes here.",
      "question_options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "The correct answer from the above options"
    }},
    ...
    (exactly 10 questions)
  ]
}}

Requirements:
- Each question must have exactly 4 distinct answer options.
- Only one correct answer is allowed per question, and it must be present in 'question_options'.
- The output must be valid JSON and parsable as-is (e.g., using Python's json.loads).
- Do not include explanations, comments, or any text outside the JSON."""


transcript = """Holy f Are you kidding me?
Sigma has just announced this lens right here for Sony for Fuji for Elmout and for Canon.
This one here is a Canon.
Sorry Nikon, but this is the 17 to 40 f 1.8 zoom lens art lens for APSC cameras.
I just instant by for me and for many many people and look at the size of it.
It is very compact.
This is the successor to the wildly popular one of the most popular lenses ever the 18 to 35 f 1.8 that they had for DSLR cameras.
So many people had that lens, some people are still Using that lens, but this one here is better than that lens in every way and it is smaller and lighter for your mirrorless cameras.
I just can't believe let's talk about it.
So I want to be clear here even though I am gushing this is not a paid or sponsored review.
This is a loner unit.
I have to send it back to Sigma.
Sigma has never paid me for anything at any time.
But I really do like their lenses and I love to review them because I get to say really good things especially about art lenses and art lens for my APSC mirrorless cameras.
I'm so happy.
A 17 to 40 f 1.8 in terms of full frame field of view is about a 25 millimeter to 60 millimeter lens f 2.7 in terms of the background separation.
So obviously that puts it extremely close to something like a 24 to 70 f 2.8 art lens when it comes to a full frame setup.
The lens in my opinion is gorgeous to look at.
I love the styling of these new Sigma lenses.
Now my Canon lens here that I am borrowing does not have an aperture ring.
The ring they say is a control ring.
You can map it to an aperture function or to other functions.
However all of the other mounts the Fuji the L mount and the Sony will have an aperture ring with the proper Numbers there and notches.
It is remarkably lightweight and compact for what it is offering 559 grams here on my scale and the zoom is all internal.
All internal zoom which will make gimbal folks Very happy.
You zoom your lens.
You're not going to get any significant weight shift in the lens itself.
So you don't have to rebalance your gimbal if you want to go from 17 to 40 that is great.
You have an auto focus to manual focus switch and two programmable focus hold buttons.
You have a rubber gasket on the back for weather sealing and a very common filter thread size of 67 millimeters.
I love that one because I have a lot of 67 millimeter filters.
You have an extremely high quality push button pedal lens hood that will help protect your lens as well as get rid of some of those pesky flares.
The focus ring is perfectly damped in my opinion and I also love the resistance of The zoom ring not too loose not too tight just right says Goldilocks.
With such a bright lens and a versatile focal length like this you can really use this lens for so many applications both photo and Video.
I certainly can use it in the studio.
Here is a shot of me Looking as handsome as all bloody get out here in the crisis center f 1.8 so even on the Canon APS-C that is a 1.6 times crop You still are going to get some background separation at 1.8 and that was shot at 17 millimeters Which is often how I would use this lens because I like to sit fairly close to my cameras to do my talking head.
However, you can zoom it all the way in to 40 millimeters and still be using f 1.8 and get some real nice Background separation, but what about performance?
Does it hold up to the art lens moniker that is stamped on this lens and Of course it does.
When it comes to auto focus. It is ridiculously fast almost instantaneous very smooth in its Transitions feels like you are using a native lens.
It is just so sticky and so reliable using the HLA motors That sigma now uses in their fancy lenses and it is just so good whether you are doing a Fc AFS or tracking it is Wonderful.
And speaking of focus when it comes to focus breathing this lens suppresses it Superbly and that is a big deal because this is a third party lens.
So if you're using Sony cameras with Sony native lenses or Canon with Canon native lenses You can use focus breathing Compensation and that can get rid of all of your focus breathing But that doesn't work with third party lenses.
So you have to rely on the lens itself not to breathe a lot and luckily this one does not at the wide and 17 millimeters or at the tight end at 40 millimeters the focus breathing is almost Non-existent so excellent job there.
Sigma knows a lot of people are gonna want to use this lens for video shooting So that is an important factor.
The lens is also extremely sharp Which is a feat of engineering because this is as sharp as many prime lenses whether you're at 17 or 40 millimeters It is exceptionally sharp in the center as well as the corners now You are going to want to use the profiles that sigma will make available.
Luckily they made them available to us reviewers ahead of time so we could see the corrections first hand because there is going to be a significant amount of vignetting and also barrel distortion on This lens in the raw format and you would expect it with a lens this size.
Kind of gone the Sony route where they're expecting the Corrections in camera or in your software to correct for the lens And that way they can make it smaller and lighter.
When you are at the wide end You will see a lot of barrel distortion as well as significant vignetting and on the long end You will see that same vignetting and pin cushion distortion.
Now if you apply those profiles it goes away Instantly so that is the price you have to pay sometimes if you want a smaller more compact lens.
Flaring is usually a category that sigma absolutely kills it and when you're talking about an art lens Of course, it doesn't bang up job here.
The coatings on the lenses are so great that if you have the most backlit subject and Just a big bright sun creeping into your image. You're still going to get amazing Contrast.
However you will see some ghosting if you are in a very challenging environment You have extremely bright midday sun going into your lens You will see some of that ghosting but it is quite neat and certainly expected for a zoom lens like this.
Now why not the largest and most dramatic sun stars I've ever seen in my life if you go to f16 You can get some nice neat sun stars in your photos.
Now. Let's look at the bouquet.
There's no point in having an f1.8 zoom lens all the way through if the bouquet is ugly and gross But it's not ugly and gross. It's amazing.
It is beautiful and it looks so good So buttery smooth the fall off from things that are in focus to out of focus just a wonderful magnificent job.
I don't know how many times I can say superlatives like this in this video, but you know sigma art 1.8 zoom lens APS-C bouquet.
Balls are nice and round in the center But once you get off center a little bit you start seeing that cats eye effect You have all those little footballs all around.
I personally don't mind that at all But if you don't like cats eye bouquet this may not be for you now.
There's a tiny bit of hallowing around the bouquet balls themselves But I think this is more than acceptable for a zoom lens of this range at 1.8.
When it comes to chromatic aberration lateral and Longitudinal with the lateral chromatic aberration You're not going to see much at all the stuff that's in the plane of focus You really don't have to worry about very much when it comes to the longitudinal chromatic aberration or Loka that is when you see areas out of focus in the foreground and background that have color fringing that is The Loka and this lens actually does a really good job on the wide end at 17 millimeters There is very minimal longitudinal chromatic aberration.
However when you zoom in all the way to 40 millimeters you will definitely see much more of it even a prime lens at 40 millimeters on an APS-C camera is likely going to struggle with a bit of Loka So the idea of having a zoom range that goes from 17 to 40 I did expect to see some here at the tighter end.
The minimum focus distance is 28 centimeters or 11.1 inches and you can get pretty close to your subject zoomed all the way into 40 millimeters really blow out that background get some nice interesting shots.
But you may be asking now that Sigma has a 17 to 40 f 1.8 Where does that leave arguably my favorite lens of all time the 18 to 50 f 2.8 from Sigma?
Well, I'll tell you where it leaves this lens right in my camera bag where it has been for quite some time.
Look at how small and compact this is compared to this 17 to 40 can you see that right there? Oh my goodness.
It is so small and light and of course you get 50 instead of 40 f 2.8 instead of 1.8.
But for me this is such a great travel lens whether it is photos or videos I love it, but especially for photos and this thing costs about 529 dollars the last time I checked so significantly cheaper as well and a much easier carry.
I can just leave this on my a6700 all the time and I am ready to go traveling even though I hate traveling.
Now I'm starting to like it more in my old age sit on a beach sip in a my tie not so bad.
With pricing now This is not confirmed check the links for the official price But they are telling me it's going to be $1250 Canadian or 919 us dollars and while that is not cheap I think that is still a great value for this lens and what it offers.
The Sony 16 to 55 is f 2.8 and that is More expensive.
This thing right here is arguably the best lens that you can get for the APS-C system for any APS-C camera it is small compact and lightweight and gives you roughly a field of view of a 24 to 70 f 2.8 sigma art lens version two.
I'm gonna say this is as good as sigma's version two 24 to 70 so really There's gonna be a lot of people lined up to buy this lens in my not so humble opinion.
So let me know down below are you even half as excited about this lens as I am because even if you're Half as excited that is still very very excited.
I love this.
I am so glad they came out with it.
I will go and pre-order my copy.
Let me know what you will do put it down there.
Well, I have a nice little discussion about it. Hey, thanks for watch."""

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=[prompt, transcript]
)
print(response.text)

