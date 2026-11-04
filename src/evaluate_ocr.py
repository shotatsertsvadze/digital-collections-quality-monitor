
def edit_distance(reference, prediction):
    previous = list(range(len(prediction) + 1))

    for i, ref_item in enumerate(reference, start=1):
        current = [i]

        for j, pred_item in enumerate(prediction, start=1):
            substitution = previous[j - 1] + (
                ref_item != pred_item
            )
            insertion = current[j - 1] + 1
            deletion = previous[j] + 1

            current.append(
                min(substitution, insertion, deletion)
            )

        previous = current

    return previous[-1]


def evaluate_text(ground_truth, ocr_text):
    if not ground_truth.strip():
        raise ValueError("Ground Truth must not be empty")

    character_errors = edit_distance(ground_truth, ocr_text)

    reference_words = ground_truth.split()
    predicted_words = ocr_text.split()

    word_errors = edit_distance(
        reference_words,
        predicted_words
    )

    return {
        "character_errors": character_errors,
        "word_errors": word_errors,
        "cer": character_errors / len(ground_truth),
        "wer": word_errors / len(reference_words),
    }


if __name__ == "__main__":
    ground_truth = "Deutscher Fesselballon zur Beobachtung"
    ocr_text = "Deutscher Fesselballon jur Beobachtung"

    result = evaluate_text(ground_truth, ocr_text)

    print("Character errors:", result["character_errors"])
    print("Word errors:", result["word_errors"])
    print(f"CER: {result['cer']:.2%}")
    print(f"WER: {result['wer']:.2%}")
