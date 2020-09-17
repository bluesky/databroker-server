import sys
from imageio import imsave


def generate_thumbnail(run, path_template):
    """
    Write one thumbnail image to represent a Run if any image-like data can be found.
    
    Logs details to the stderr.
    
    Parameters
    ----------
    run: BlueskyRun
    path_template: str
        May include templates like {start[plan_name]} or {stop[exit_status]}
        which will be extracted from the documents. If it does not end in ".png", then
        ".png" will be appended to the path.
    
    Returns
    -------
    path: str or None
        The (possibly templated) path or, if no image data was found, None
        
    Examples
    --------
    Write a PNG to a simple path.
    
    >>> generate_thumbnail(catalog[-1], "/tmp/test_thumbnail.png") 
    Wrote 'img' from Run a907fe84 to /tmp/test_thumbnail.png
    '/tmp/test_thumbnail.png'

    Write a PNG to a path created by templating metadata from the Run.
    
    >>> generate_thumbnail(catalog[-1], "/tmp/test_thumbnail_{start[uid]:.8}_{start[plan_name]}.png")                                                                                  
    Wrote 'img' from Run a907fe84 /tmp/test_thumbnail_a907fe84_count.png
    '/tmp/test_thumbnail_a907fe84_count.png'

    """
    if not path_template.endswith(".png"):
        path_template += ".png"
    path = path_template.format(**run.metadata)
    uid = run.metadata['start']['uid']
    if 'primary' in run:
        stream_name = 'primary'
    elif list(run):
        # Just grab the first stream.
        stream_name = list(run)[0]
    else:
        print(f"No image data found in Run {uid:.8}", file=sys.stderr)
    dataset = run[stream_name].to_dask()
    # Find the first column that looks like an image.
    # Grab a slice from the middle because that is most likely to be interesting.
    for column in dataset:
        xarr = dataset[column]
        if xarr.ndim == 3:  # a column of single images
            image = dataset[column][xarr.shape[0] // 2]
            break
        elif xarr.ndim == 4:  # a column of stacks of images (like Area Detector gives)
            image = dataset[column][xarr.shape[0] // 2, xarr.shape[1] // 2]
            break
    else:
        print(f"No image data found in Run {uid:.8}", file=sys.stderr)
        return None
    im = image.data.compute()
    im = im - im.min()
    im = im * (1.0 / im.max() * 255)
    print("Image min/max: ", im.min(), im.max())
    imsave(path, im)
    print(f"Wrote {column!r} from Run {uid:.8} to {path}", file=sys.stderr)
    return path
