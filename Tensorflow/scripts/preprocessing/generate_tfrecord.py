import tensorflow as tf
import os
import xml.etree.ElementTree as ET


def create_tf_example(xml_file, label_map):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    filename = root.find('filename').text
    width = int(root.find('size/width').text)
    height = int(root.find('size/height').text)

    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for member in root.findall('object'):
        classes_text.append(member[0].text.encode('utf8'))
        classes.append(label_map[member[0].text])

        xmin = float(member.find('bndbox/xmin').text) / width
        ymin = float(member.find('bndbox/ymin').text) / height
        xmax = float(member.find('bndbox/xmax').text) / width
        ymax = float(member.find('bndbox/ymax').text) / height

        xmins.append(xmin)
        ymins.append(ymin)
        xmaxs.append(xmax)
        ymaxs.append(ymax)

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': tf.train.Feature(int64_list=tf.train.Int64List(value=[height])),
        'image/width': tf.train.Feature(int64_list=tf.train.Int64List(value=[width])),
        'image/filename': tf.train.Feature(bytes_list=tf.train.BytesList(value=[filename.encode('utf8')])),
        'image/object/bbox/xmin': tf.train.Feature(float_list=tf.train.FloatList(value=xmins)),
        'image/object/bbox/xmax': tf.train.Feature(float_list=tf.train.FloatList(value=xmaxs)),
        'image/object/bbox/ymin': tf.train.Feature(float_list=tf.train.FloatList(value=ymins)),
        'image/object/bbox/ymax': tf.train.Feature(float_list=tf.train.FloatList(value=ymaxs)),
        'image/object/class/text': tf.train.Feature(bytes_list=tf.train.BytesList(value=classes_text)),
        'image/object/class/label': tf.train.Feature(int64_list=tf.train.Int64List(value=classes)),
    }))
    return tf_example


def process_dataset(directory, output_filename, label_map):
    writer = tf.io.TFRecordWriter(output_filename)

    for xml_file in os.listdir(directory):
        if xml_file.endswith('.xml'):
            path = os.path.join(directory, xml_file)
            tf_example = create_tf_example(path, label_map)
            writer.write(tf_example.SerializeToString())

    writer.close()
    print(f"Successfully created the TFRecords: {output_filename}")


def main():
    label_map = {'stop': 1, 'volumeup': 2, 'volumedown': 3, 'collapsed': 4, 'full': 5}

    train_dir = r'C:\Users\Dmitry\PycharmProjects\gesture16\Tensorflow\workspace\training_demo\images\test'
    test_dir = r'C:\Users\Dmitry\PycharmProjects\gesture16\Tensorflow\workspace\training_demo\images\train'

    process_dataset(train_dir, 'train.record', label_map)
    process_dataset(test_dir, 'test.record', label_map)

if __name__ == '__main__':
    main()
