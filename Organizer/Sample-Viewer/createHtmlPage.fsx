// Running the following lines in F# interactive will create three files:
// - training.png
// - validation.png
// - digits.html
//
// Note:
// - run "PossibleSolution.fsx" before running this script
// - the file "digits.html.template" is expected to be in the current directory
// - the new files will be created in the current directory

open System.IO
open System.Drawing
open System.Drawing.Imaging

let (width, height) = (28, 28)
let digitsPerRow = 100

let offset idx = (idx % digitsPerRow * width), (idx / digitsPerRow * height)

// Store array of digits as a single PNG image.
let saveAsPng (digits: Observation[]) (fileName: string) =
    let len = digits.Length
    let rows = (len + digitsPerRow - 1) / digitsPerRow

    use bmp = new Bitmap(digitsPerRow * width, rows * height)
    let drawDigit digit (x, y) =
        let colors = [|0..255|] |> Array.map (fun c -> Color.FromArgb (c, c, c))
        let drawPixel i p = bmp.SetPixel (x + i % width, y + i / width, colors.[p])
        digit.Pixels |> Array.iteri drawPixel

    digits |> Array.iteri (fun i d -> drawDigit d (offset i))
    bmp.Save(fileName, ImageFormat.Png)

saveAsPng training "training.png"
saveAsPng validation "validation.png"

// Create HTML page by populating the template.
let populateWithDigits digits name (text: string) =
    let items = digits |> Array.mapi (fun i d ->
        let (x, y) = offset i
        sprintf "<li><div style='background-position: -%dpx -%dpx'></div><label>%d</label></li>" x y d.Label)
    text.Replace (sprintf "{%s}" name, String.concat "\n" items)

let html =
    File.ReadAllText("digits.html.template")
    |> populateWithDigits training "training"
    |> populateWithDigits validation "validation"

File.WriteAllText("digits.html", html)
